from debug_toolbar.panels import Panel
from django.db import connection
from django.templatetags.static import static

class AssistantPanel(Panel):
    title = "Assistant"
    has_content = True
    template = "panels/djdt_assistant.html"
    
    @property
    def scripts(self):
        return [
            static("__debug__/djdt_assistant_panel/js/panel.js")
        ]
