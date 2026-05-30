import * as vscode from 'vscode';
import { PythonBridge } from './pythonBridge';

export class PluginsTreeProvider implements vscode.TreeDataProvider<PluginItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<PluginItem | undefined | null | void>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    constructor(private pythonBridge: PythonBridge) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: PluginItem): vscode.TreeItem {
        return element;
    }

    async getChildren(element?: PluginItem): Promise<PluginItem[]> {
        if (!element) {
            // Root level - show all plugins
            try {
                const catalog = await this.pythonBridge.getCatalog();
                const plugins = (catalog.plugins || []).map((p: any) =>
                    new PluginItem(
                        p.name,
                        p.description,
                        p.category || 'general',
                        vscode.TreeItemCollapsibleState.None
                    )
                );
                return plugins;
            } catch (error) {
                return [new PluginItem('Error loading plugins', '', '', vscode.TreeItemCollapsibleState.None)];
            }
        }
        return [];
    }
}

class PluginItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly description: string,
        public readonly category: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState
    ) {
        super(label, collapsibleState);
        this.tooltip = description;
        this.contextValue = 'plugin';

        // Make plugin items clickable to scaffold
        if (collapsibleState === vscode.TreeItemCollapsibleState.None) {
            this.command = {
                command: 'agenticq.scaffoldPlugin',
                title: 'Scaffold Plugin',
                arguments: [label]
            };
        }
    }
}
