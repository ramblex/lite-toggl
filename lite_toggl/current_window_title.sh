#!/bin/bash

# Retrieves the current active window title

xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) _NET_WM_NAME | awk -F '"' '{print $2}'
