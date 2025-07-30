#!/bin/bash
clear
rm -r dist/

export SKBUILD_KEEP_TEMP=1
SKBUILD_KEEP_TEMP=1 python -m build
