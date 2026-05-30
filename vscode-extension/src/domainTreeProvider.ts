import * as vscode from 'vscode';
import { PythonBridge } from './pythonBridge';

export class DomainTreeProvider implements vscode.TreeDataProvider<DomainItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<DomainItem | undefined | null | void>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    constructor(private pythonBridge: PythonBridge) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: DomainItem): vscode.TreeItem {
        return element;
    }

    async getChildren(element?: DomainItem): Promise<DomainItem[]> {
        if (!element) {
            // Root level - show domains
            try {
                const catalog = await this.pythonBridge.getCatalog();
                const domains = new Map<string, string[]>();

                // Group plugins by category
                for (const plugin of catalog.plugins || []) {
                    const category = plugin.category || 'general';
                    if (!domains.has(category)) {
                        domains.set(category, []);
                    }
                    domains.get(category)?.push(plugin.name);
                }

                return Array.from(domains.entries()).map(([category, plugins]) =>
                    new DomainItem(
                        category,
                        `${plugins.length} plugins`,
                        vscode.TreeItemCollapsibleState.Collapsed
                    )
                );
            } catch (error) {
                return [new DomainItem('Error loading domains', '', vscode.TreeItemCollapsibleState.None)];
            }
        } else {
            // Show plugins in domain
            try {
                const catalog = await this.pythonBridge.getCatalog();
                const plugins = (catalog.plugins || [])
                    .filter((p: any) => (p.category || 'general') === element.label)
                    .map((p: any) => new DomainItem(
                        p.name,
                        p.description,
                        vscode.TreeItemCollapsibleState.None
                    ));
                return plugins;
            } catch (error) {
                return [];
            }
        }
    }
}

class DomainItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly description: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState
    ) {
        super(label, collapsibleState);
        this.tooltip = description;
    }
}
