# BDcraft-mod-packer

Thanks to [ndrplz](https://github.com/ndrplz) and [google-drive-downloader](https://github.com/ndrplz/google-drive-downloader)

## Intro
A tool to download all mod patch texture packs from [BDcraft.net](https://bdcraft.net) and pack them into one zip file.

## Requirement

You need to have fairy access to Google Drive, or some texture packs may not be downloaded.

## Install

```bash
pip install bdcraft-mod-packer
```

## Usage

Run the command below and wait it to finish.

```bash
python -m bdcraft_mod_packer
```

When finished, the combined texture pack will lay in the `out` dir

## Default Parameters

```bash
--mc-version: 1.12

--output: out

--resolution: 128x
```
