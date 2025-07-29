from django.apps import AppConfig

class AssistantPanelConfig(AppConfig):
    name = "django_debug_toolbar_assistant_panel"

    def ready(self):
        import debug_toolbar.panels
        from debug_toolbar.toolbar import DebugToolbar
        from .panel import AssistantPanel

        DebugToolbar._panel_classes.append(AssistantPanel)
