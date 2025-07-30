# Prune's Captcha

## What is it for?

Captcha helps prevent robots from spamming using your forms.

## Prerequisites

-   To be installed on a Prune Django project that uses poetry or UV

## UV project

### Installation

Run the following command in the console:

```bash
uv add captcha_prune
```

### Updating the captcha

Don't hesitate to regularly run `uv sync --upgrade`, as the captcha evolves with time and our practices!

## Poetry project

### Installation

Run the following command:

```bash
poetry add prune_captcha
```

### Updating the captcha

Don't hesitate to regularly run `poetry update`, as the captcha evolves with time and our practices!

## Captcha Integration

### Configuration

In `settings.py`, set the path to the images used for the puzzle:

```python
PUZZLE_IMAGE_STATIC_PATH = "website/static/website/images/"
```

### Utilisation

-   GET request (form display)

    -   Use create_captcha_view to generate the captcha data:

        ```python
        from captcha_prune.views import create_captcha_view
        ```

        ```python
        puzzle = create_captcha_view(request)
        ```

    -   Passes the data into the context under the puzzle variable:

        ```python
        return render(
            request,
            "website/pages/contact/page.html",
            {"form": form, "puzzle": puzzle},
        )
        ```

    -   Include the component in your template:

        ```
        {% include "captcha_prune/captcha.html" %}
        ```

-   POST request (form submission)

        -   Use verify_captcha_view to validate the captcha:

            ```python
            from captcha_prune.views import verify_captcha_view
            ```

            ```python
            response = verify_captcha_view(request)
            ```

        -   True if the captcha is correct, else False.

        -   Redirects in case of expired session or incorrect captcha:

            ```python
            if response is False:
                return redirect("website:contact-page")
            ```

### Example

    ```python
    def contact_view(request):
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                response = verify_captcha_view(request)
            if response is False:
                return redirect("website:contact-page")
            messages.success(request, "Formulaire soumis avec succès.")
            return redirect("/")
        else:
            puzzle = create_captcha_view(request)
    else:
        form = ContactForm()
        puzzle = create_captcha_view(request)
    return render(
        request,
        "website/pages/contact/page.html",
        {"form": form, "puzzle": puzzle},
    )
    ```

# Available Versions

| Version | Date       | Notes                              |
| ------- | ---------- | ---------------------------------- |
| 1.11.0  | 2025-05-21 | removed utils                      |
| 1.10.0  | 2025-05-20 | fix documentation, removed ...     |
| 1.9.0   | 2025-05-20 | puzzle images path fixed           |
| 1.8.0   | 2025-05-20 | added migrations                   |
| 1.7.0   | 2025-05-20 | PUZZLE_IMAGE_STATIC_PATH ...       |
| 1.6.0   | 2025-05-20 | added templates                    |
| 1.5.0   | 2025-05-20 | app config fixed, components ...   |
| 1.4.0   | 2025-05-20 | added BaseModel in Captcha, ...    |
| 1.3.0   | 2025-04-30 | deleted start_server, deleted ...  |
| 1.2.0   | 2025-04-30 | fixed prune_captcha command, ...   |
| 1.1.0   | 2025-04-30 | start_server was not a module, ... |
| 1.0.0   | 2025-04-29 | First version of the `captcha` ... |
