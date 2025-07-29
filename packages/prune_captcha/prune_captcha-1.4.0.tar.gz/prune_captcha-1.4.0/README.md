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
PUZZLE_IMAGE_STATIC_PATH = "website/images/"
```

### Utilisation

-   GET request (form display)

    -   Use create_and_get_puzzle to generate the captcha data.

    -   Passes the data into the context under the puzzle variable.

    -   Include the component in your template:

        ```python
        from captcha_prune.utils import create_and_get_puzzle
        ```

        ```
        {% include "captcha_prune/components/captcha.html" %}
        ```

-   POST request (form submission)

        -   Use verify_captcha to validate the captcha.

            ```python
            from captcha_prune.utils import verify_captcha
            ```

            ```python
            verify_captcha(request, redirect("/"), redirect("website:contact-page"), form)
            ```

        -   No feedback if the captcha is correct.

        -   Redirects in case of expired session or incorrect captcha.

### Example

    ```python
    from django.shortcuts import render, redirect

    from django.contrib import messages
    from captcha_prune.utils import create_and_get_puzzle, verify_captcha
    from .forms import ContactForm

    def contact_view(request):
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                verify_captcha(
                    request,
                    redirect("/"),
                    redirect("website:contact-page"),
                    form
                )
                messages.success(request, "Formulaire soumis avec succès.")
                return redirect("/")
            else:
                puzzle = create_and_get_puzzle(request)
        else:
            form = ContactForm()
            puzzle = create_and_get_puzzle(request)
    return render(
        request,
        "website/pages/contact/page.html",
        {"form": form, "puzzle": puzzle},
    )

```

# Available Versions

| Version | Date       | Notes                              |
| ------- | ---------- | ---------------------------------- |
| 1.4.0   | 2025-05-20 | added BaseModel in Captcha, ...    |
| 1.3.0   | 2025-04-30 | deleted start_server, deleted ...  |
| 1.2.0   | 2025-04-30 | fixed prune_captcha command, ...   |
| 1.1.0   | 2025-04-30 | start_server was not a module, ... |
| 1.0.0   | 2025-04-29 | First version of the `captcha` ... |
```
