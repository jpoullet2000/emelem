#!/usr/bin/env bash
rm -rf _build
make html
cp -r ../emelem/assets/images/ _static/img/
rm -rf /tmp/emelem-docs
cp -r _build/html /tmp/emelem-docs
