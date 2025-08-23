# JupyterLab Configuration for AI/Copilot Integration
# This configuration file enables the best AI assistance features in JupyterLab

c = get_config()

# Enable LSP (Language Server Protocol) for better code intelligence
c.LanguageServerManager.language_servers = {
    'python-lsp-server': {
        'version': 2,
        'argv': ['python-lsp-server'],
        'languages': ['python'],
        'mime_types': ['text/x-python'],
    }
}

# Enable code formatting
c.ServerApp.jpserver_extensions = {
    'jupyterlab_code_formatter': True,
    'jupyterlab_github': True,
    'jupyterlab_lsp': True
}

# Set up better kernel management
c.MultiKernelManager.default_kernel_name = 'python3'

# Enable collaborative features
c.ServerApp.collaborative = True

print("JupyterLab configuration loaded with AI assistance features!")
