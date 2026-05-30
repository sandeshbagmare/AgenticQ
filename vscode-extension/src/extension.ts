import * as vscode from 'vscode';
import { PythonBridge } from './pythonBridge';
import { DomainTreeProvider } from './domainTreeProvider';

let pythonBridge: PythonBridge | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('AgenticQ extension is now active');

    // Initialize Python bridge
    pythonBridge = new PythonBridge();

    // Register tree providers
    const domainProvider = new DomainTreeProvider(pythonBridge);
    vscode.window.registerTreeDataProvider('agenticqDomains', domainProvider);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('agenticq.scaffold', async () => {
            const plugins = await vscode.window.showInputBox({
                prompt: 'Enter plugin names (comma-separated)',
                placeHolder: 'python-development, unit-testing'
            });

            if (plugins) {
                const pluginList = plugins.split(',').map(p => p.trim());
                const harness = await vscode.window.showQuickPick(
                    ['claude-code', 'cursor', 'gemini', 'codex', 'opencode', 'copilot'],
                    { placeHolder: 'Select target harness' }
                );

                if (harness && vscode.workspace.workspaceFolders) {
                    const targetDir = vscode.workspace.workspaceFolders[0].uri.fsPath;

                    vscode.window.withProgress({
                        location: vscode.ProgressLocation.Notification,
                        title: 'Scaffolding plugins...',
                        cancellable: false
                    }, async () => {
                        try {
                            const result = await pythonBridge?.scaffold(pluginList, harness, targetDir);
                            if (result?.success) {
                                vscode.window.showInformationMessage(`✓ ${result.message}`);
                            } else {
                                vscode.window.showErrorMessage(`✗ ${result?.message || 'Scaffolding failed'}`);
                            }
                        } catch (error) {
                            vscode.window.showErrorMessage(`Error: ${error}`);
                        }
                    });
                }
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('agenticq.recommend', async () => {
            if (!vscode.workspace.workspaceFolders) {
                vscode.window.showErrorMessage('No workspace folder open');
                return;
            }

            const targetDir = vscode.workspace.workspaceFolders[0].uri.fsPath;

            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: 'Analyzing project...',
                cancellable: false
            }, async () => {
                try {
                    const recommendations = await pythonBridge?.recommend(targetDir);

                    if (recommendations && recommendations.length > 0) {
                        const items: vscode.QuickPickItem[] = recommendations.map((rec: any) => ({
                            label: rec.plugin_name,
                            description: `Score: ${rec.relevance_score.toFixed(1)} | Tokens: ${rec.token_cost_estimate}`,
                            detail: rec.reason
                        }));

                        const selected = await vscode.window.showQuickPick(items, {
                            placeHolder: 'Select plugins to scaffold',
                            canPickMany: true
                        });

                        if (selected && selected.length > 0) {
                            const pluginNames = selected.map(item => item.label);
                            const harness = await vscode.window.showQuickPick(
                                ['claude-code', 'cursor', 'gemini', 'codex', 'opencode', 'copilot'],
                                { placeHolder: 'Select target harness' }
                            );

                            if (harness) {
                                const result = await pythonBridge?.scaffold(pluginNames, harness, targetDir);
                                if (result?.success) {
                                    vscode.window.showInformationMessage(`✓ ${result.message}`);
                                } else {
                                    vscode.window.showErrorMessage(`✗ ${result?.message || 'Scaffolding failed'}`);
                                }
                            }
                        }
                    } else {
                        vscode.window.showInformationMessage('No recommendations found');
                    }
                } catch (error) {
                    vscode.window.showErrorMessage(`Error: ${error}`);
                }
            });
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('agenticq.browse', () => {
            domainProvider.refresh();
            vscode.window.showInformationMessage('Domain browser refreshed');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('agenticq.openWebview', () => {
            const panel = vscode.window.createWebviewPanel(
                'agenticqDashboard',
                'AgenticQ Dashboard',
                vscode.ViewColumn.One,
                { enableScripts: true }
            );

            panel.webview.html = getWebviewContent();
        })
    );
}

export function deactivate() {
    if (pythonBridge) {
        pythonBridge.dispose();
    }
}

function getWebviewContent(): string {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgenticQ Dashboard</title>
    <style>
        body { font-family: var(--vscode-font-family); padding: 20px; }
        h1 { color: var(--vscode-foreground); }
        .domain-card {
            border: 1px solid var(--vscode-panel-border);
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>AgenticQ Dashboard</h1>
    <p>Use the commands in the Command Palette to interact with AgenticQ.</p>
    <div id="content"></div>
</body>
</html>`;
}
