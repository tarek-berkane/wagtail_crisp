from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HeaderBlock(blocks.StructBlock):
    HEADER_TYPE = (
        ("h2", "head 2"),
        ("h3", "head 3"),
        ("h4", "head 4"),
    )

    head_type = blocks.ChoiceBlock(choices=HEADER_TYPE, default="h2", max_length=2)
    title = blocks.CharBlock(max_length=255)

    class Meta:
        template = "post/blocks/head.html"


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(max_length=50, required=False)

    class Meta:
        template = "post/blocks/image.html"


class QuoteBlock(blocks.StructBlock):
    text = blocks.TextBlock()

    class Meta:
        template = "post/blocks/blockquote.html"


class CodeBlock(blocks.StructBlock):
    CODE_TYPE = (
        ("py", "Python"),
        ("js", "Javascript"),
        ("java", "Java"),
        ("html", "html"),
        ("dart", "Dart"),
        ("c", "C"),
    )

    code_type = blocks.ChoiceBlock(choices=CODE_TYPE, default="py")
    code = blocks.TextBlock()

    class Meta:
        template = "post/blocks/code.html"
