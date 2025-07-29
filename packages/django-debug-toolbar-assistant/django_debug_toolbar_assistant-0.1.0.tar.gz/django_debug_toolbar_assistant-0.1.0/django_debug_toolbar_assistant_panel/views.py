# django_debug_toolbar_query_assistant_panel/views.py
import uuid
import json
import google.generativeai as genai
import markdown
import gzip
import base64

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.cache import cache
from django.conf import settings

CONTEXT_TTL_SECONDS = 60 * 30  # 30 minutes

genai.configure()

@csrf_exempt
@require_POST
def upload_context(request):
    try:
        body = json.loads(request.body)
        context_html = body.get("context", "")
        if not context_html:
            return HttpResponseBadRequest("Missing context")

        context_id = str(uuid.uuid4())

        # Compress and encode
        compressed = gzip.compress(context_html.encode("utf-8"))
        b64 = base64.b64encode(compressed).decode("utf-8")

        cache.set(f"context:{context_id}", b64, timeout=CONTEXT_TTL_SECONDS)
        return JsonResponse({"context_id": context_id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_POST
def llm_chat(request):
    try:
        data = json.loads(request.body)
        context_id = data.get("context_id")
        messages = data.get("messages", [])

        if not context_id or not messages:
            return HttpResponseBadRequest("Missing context_id or messages")

        b64 = cache.get(f"context:{context_id}")
        if not b64:
            return HttpResponseBadRequest("Context not found or expired")

        compressed = base64.b64decode(b64)
        context = gzip.decompress(compressed).decode("utf-8")

        if not context:
            return HttpResponseBadRequest("Context not found or expired")

        user_input = messages[-1]["content"]

        # Prepare full prompt with context
        prompt = f"""You are an expert assistant helping debug Django applications.

Below is the context, consisting of HTML output from the Django Debug Toolbar. Use this to understand the app’s runtime behavior, SQL queries, settings, and stack traces.

When responding:
- Format your response as **valid markdown**.
- When including code examples, use **fenced code blocks**, **but DO NOT specify a language** (i.e., no `python`, `html`, etc.).
- Ensure that code formatting does not interfere with surrounding markdown — avoid malformed or broken formatting.
- Keep explanations clear, structured, and concise.

---------------------
{context}
---------------------

Now answer the following question:

{user_input}
"""
        model_name = data.get("model", "gemini-1.5-flash")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        answer = response.text.strip()
        html_answer = markdown.markdown(answer, extensions=["fenced_code"])

        return JsonResponse({"response": html_answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)