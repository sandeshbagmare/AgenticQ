import { spawn, ChildProcess } from 'child_process';
import * as vscode from 'vscode';

export class PythonBridge {
    private process: ChildProcess | undefined;
    private requestId = 0;
    private pendingRequests = new Map<number, { resolve: Function; reject: Function }>();

    constructor() {
        this.start();
    }

    private start() {
        const config = vscode.workspace.getConfiguration('agenticq');
        const pythonPath = config.get<string>('pythonPath', 'python');

        // Try spawning with configured python path + module invocation
        this.process = spawn(pythonPath, ['-m', 'agenticq', 'serve', '--jsonrpc'], {
            stdio: ['pipe', 'pipe', 'pipe']
        });

        // Handle spawn errors (e.g., ENOENT if python not found)
        this.process.on('error', (error) => {
            console.error('Failed to spawn agenticq:', error);
            vscode.window.showErrorMessage(
                `AgenticQ: Failed to start Python backend. ` +
                `Ensure Python and agenticq are installed. Error: ${error.message}`
            );
            // Reject all pending requests
            for (const [id, pending] of this.pendingRequests.entries()) {
                pending.reject(new Error('Python bridge failed to start'));
                this.pendingRequests.delete(id);
            }
        });

        if (this.process.stdout) {
            this.process.stdout.on('data', (data) => {
                const lines = data.toString().split('\n');
                for (const line of lines) {
                    if (line.trim()) {
                        try {
                            const response = JSON.parse(line);
                            this.handleResponse(response);
                        } catch (error) {
                            console.error('Failed to parse response:', error);
                        }
                    }
                }
            });
        }

        if (this.process.stderr) {
            this.process.stderr.on('data', (data) => {
                console.error('Python bridge error:', data.toString());
            });
        }

        this.process.on('exit', (code, signal) => {
            console.log(`Python bridge exited with code ${code}, signal ${signal}`);
            // Reject all pending requests
            for (const [id, pending] of this.pendingRequests.entries()) {
                pending.reject(new Error('Python bridge process exited'));
                this.pendingRequests.delete(id);
            }
        });
    }

    private handleResponse(response: any) {
        const id = response.id;
        const pending = this.pendingRequests.get(id);

        if (pending) {
            if (response.error) {
                pending.reject(new Error(response.error.message));
            } else {
                pending.resolve(response.result);
            }
            this.pendingRequests.delete(id);
        }
    }

    private sendRequest(method: string, params: any = {}): Promise<any> {
        return new Promise((resolve, reject) => {
            const id = ++this.requestId;
            const request = {
                jsonrpc: '2.0',
                id,
                method,
                params
            };

            this.pendingRequests.set(id, { resolve, reject });

            if (this.process && this.process.stdin) {
                this.process.stdin.write(JSON.stringify(request) + '\n');
            } else {
                reject(new Error('Python bridge not started'));
            }

            // Timeout after 30 seconds
            setTimeout(() => {
                if (this.pendingRequests.has(id)) {
                    this.pendingRequests.delete(id);
                    reject(new Error('Request timeout'));
                }
            }, 30000);
        });
    }

    async getCatalog(): Promise<any> {
        return this.sendRequest('catalog/list');
    }

    async scanProject(path: string): Promise<any> {
        return this.sendRequest('project/scan', { path });
    }

    async recommend(path: string, maxResults: number = 10): Promise<any> {
        return this.sendRequest('recommend', { path, max_results: maxResults });
    }

    async scaffold(plugins: string[], harness: string, target: string): Promise<any> {
        return this.sendRequest('scaffold', { plugins, harness, target });
    }

    dispose() {
        if (this.process) {
            this.process.kill();
        }
    }
}
