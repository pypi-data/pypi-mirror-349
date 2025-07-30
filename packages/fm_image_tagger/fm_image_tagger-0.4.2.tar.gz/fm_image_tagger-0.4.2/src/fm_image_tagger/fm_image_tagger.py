import click

import fm_image_tagger.command_tagger as command_tagger
import fm_image_tagger.display as Display
import fm_image_tagger.rename as Rename
import fm_image_tagger.tag_edit as Editor
import fm_image_tagger.total as Total


# CLI main function
@click.group()
def cli():
    pass


@cli.command(help="Create tag files")
@click.argument("path", type=str)
@click.option(
    "-t", "--threshold", default=0.35, help="score threshold (default:0.35)", type=float
)
def tagger(path, threshold):
    command_tagger.createTagFiles(path, threshold)


@cli.command(help="Create caption files, use Ollama vision-model")
@click.argument("ollama-vision-model", type=str)
@click.argument("path", type=str)
@click.option("-l", "--for-lora", is_flag=True, help="LoRA caption mode")
def caption(ollama_vision_model, path, for_lora):
    command_tagger.createCaptionFiles(path, ollama_vision_model, for_lora)


@cli.command(help="Rename with the serial number")
@click.argument("suffix", type=str)
@click.argument("path", type=str)
def rename(suffix, path):
    Rename.rename_files(path, suffix)


@cli.command(help="add word to tag files")
@click.argument("keyword", type=str)
@click.argument("path", type=str)
@click.option("-f", "--first", is_flag=True, help="Add to tags top")
def add(keyword, path, first):
    Editor.add(path, keyword, first)


@cli.command(help="remove word from tag files")
@click.argument("keywords", type=str, nargs=-1)
@click.argument("path", type=str)
def remove(keywords, path):
    Editor.remove(path, keywords)


@cli.command(help="remove word from tag files")
@click.argument("path", type=str)
def total(path):
    Total.total(path)


@cli.command(help="display picture information")
@click.argument("path", type=str)
@click.option("-m", "--meta", is_flag=True, help="display prompt in metainfo")
@click.option(
    "-t", "--threshold", default=0.35, help="score threshold (default:0.35)", type=float
)
@click.option(
    "-c",
    "--caption-model",
    default="",
    help="Caption display when Ollama model is specified",
    type=str,
)
@click.option("-l", "--for-lora", is_flag=True, help="LoRA caption mode")
def display(path, meta, threshold, caption_model, for_lora):
    if len(caption_model) > 0:
        Display.caption(path, caption_model, for_lora)
    else:
        Display.display(path, meta, threshold=threshold)


# cli app entry point
def run():
    cli()
