# Window Actions Elgato Plugin

[![Marketplace download badge](https://img.shields.io/badge/dynamic/json?logo=data:image/svg%2bxml;base64,PHN2ZyB3aWR0aD0iMjMwIiBoZWlnaHQ9IjIzMCIgdmlld0JveD0iMCAwIDIzMCAyMzAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik02My45NzEgMzguNDgzTDY0LjA5MSAzOC41NzNMMTA5LjY5MiA2NC43NzdDMTA3LjQ1MyA3Ny4yODUgMTAwLjg5NCA4OC43MTIgOTEuMTgzIDk2Ljk3NkM4MS4zMTYgMTA1LjM3MyA2OC43NDkgMTEwIDU1Ljc5MSAxMTBDNDEuMTU5IDExMCAyNy40MDMgMTA0LjI4IDE3LjA1IDkzLjg5MUM2LjcwMiA4My41MDIgMSA2OS42ODYgMSA1NUMxIDQwLjMxNCA2LjcwMiAyNi40OTggMTcuMDQ5IDE2LjEwOUMyNy4zOTYgNS43MiA0MS4xNTIgMCA1NS43OSAwQzY2Ljk3MSAwIDc3LjcyIDMuMzYxIDg2Ljg3OSA5LjcxMUM5NS44MjggMTUuOTE3IDEwMi42NzYgMjQuNTQxIDEwNi42OTEgMzQuNjU0QzEwNy4yMDEgMzUuOTUgMTA3LjY3NSAzNy4yODMgMTA4LjA4OSAzOC42MjFMOTguMzQ4IDQ0LjI4N0M5OC4wMTIgNDIuOTQzIDk3LjYxIDQxLjYwNCA5Ny4xNDggNDAuMzAyQzkwLjk0MiAyMi43NDcgNzQuMzE3IDEwLjk0NyA1NS43OSAxMC45NDdDMzEuNTkxIDEwLjk0NyAxMS45MDUgMzAuNzExIDExLjkwNSA1NUMxMS45MDUgNzkuMjg5IDMxLjU5MSA5OS4wNTMgNTUuNzkgOTkuMDUzQzY1LjE5NCA5OS4wNTMgNzQuMTYyIDk2LjEgODEuNzMgOTAuNTA3Qzg5LjE0MiA4NS4wMjcgOTQuNTc5IDc3LjUxOSA5Ny40NTQgNjguNzk5TDk3LjQ4NCA2OC42MDdMNDQuMzAyIDM4LjA2NFY3MS4xODJMNjIuNjM3IDYwLjU3N0w3Mi4wNzggNjUuOTkxTDQ0LjU5NiA4MS44ODlMMzQuODc5IDc2LjMzMVYzMi45NzRMNDQuNTg0IDI3LjM2Mkw2My45NzYgMzguNDg5TDYzLjk3IDM4LjQ4M0g2My45NzFaIiBmaWxsPSJ3aGl0ZSIvPgo8ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfMTFfNDU2KSI+CjxwYXRoIGQ9Ik0yMzAgOTBDMjMwIDEwMS4wNDYgMjIxLjA0NiAxMTAgMjEwIDExMEMyMDUuOTQyIDExMCAyMDIuMTY2IDEwOC43OTIgMTk5LjAxMyAxMDYuNzE1QzE5NS44NiAxMDQuNjM4IDE5My4zMjkgMTAxLjY5MiAxOTEuNzYyIDk4LjIxOUwxNzcuMjggNjYuMTMxQzE3Ni44ODggNjUuMjYzIDE3Ni4wMTYgNjQuNjU4IDE3NS4wMDEgNjQuNjU4QzE3My45ODYgNjQuNjU4IDE3My4xMTMgNjUuMjY0IDE3Mi43MjIgNjYuMTMzTDE1OC4yNCA5OC4yMTlDMTU1LjEwNSAxMDUuMTY2IDE0OC4xMTggMTEwIDE0MC4wMDEgMTEwQzEyOC45NTYgMTEwIDEyMC4wMDEgMTAxLjA0NiAxMjAuMDAxIDkwQzEyMC4wMDEgODUuOTQyIDEyMS4yMSA4Mi4xNjYgMTIzLjI4NyA3OS4wMTNDMTI1LjM2NCA3NS44NiAxMjguMzEgNzMuMzMgMTMxLjc4MyA3MS43NjJMMTYzLjg3MSA1Ny4yOEMxNjQuNzM5IDU2Ljg4OCAxNjUuMzQzIDU2LjAxNSAxNjUuMzQzIDU1QzE2NS4zNDMgNTMuOTg1IDE2NC43MzggNTMuMTEyIDE2My44NjkgNTIuNzIxTDEzMS43ODIgMzguMjM5QzEyNC44MzUgMzUuMTA0IDEyMCAyOC4xMTcgMTIwIDIwQzEyMCA4Ljk1NSAxMjguOTU1IDAgMTQwIDBDMTQ0LjA1OSAwIDE0Ny44MzUgMS4yMDkgMTUwLjk4OCAzLjI4NkMxNTQuMTQxIDUuMzYzIDE1Ni42NzEgOC4zMDggMTU4LjIzOSAxMS43ODJMMTcyLjcyMSA0My44N0MxNzMuMTEzIDQ0LjczOCAxNzMuOTg2IDQ1LjM0MiAxNzUgNDUuMzQyQzE3Ni4wMTQgNDUuMzQyIDE3Ni44ODkgNDQuNzM3IDE3Ny4yOCA0My44NjhMMTkxLjc2MiAxMS43ODJDMTk0Ljg5NyA0LjgzNSAyMDEuODg0IDAgMjEwIDBDMjIxLjA0NiAwIDIzMCA4Ljk1NSAyMzAgMjBDMjMwIDI0LjA1OCAyMjguNzkxIDI3LjgzNCAyMjYuNzE0IDMwLjk4OEMyMjQuNjM3IDM0LjE0MSAyMjEuNjkyIDM2LjY3MiAyMTguMjE5IDM4LjIzOUwxODYuMTMzIDUyLjcyMUMxODUuMjY0IDUzLjExMiAxODQuNjU4IDUzLjk4NSAxODQuNjU4IDU1QzE4NC42NTggNTYuMTQgMTg1LjM4NiA1Ni45NDMgMTg2LjEzMSA1Ny4yOEwyMTguMjE5IDcxLjc2MkMyMjUuMTY1IDc0Ljg5NyAyMzAgODEuODg0IDIzMCA5MFoiIGZpbGw9IiM0RERBNzkiLz4KPC9nPgo8cGF0aCBkPSJNMTIuNTAxIDEyNUM1LjU5NyAxMjUgMC4wMDEgMTMwLjU5NiAwLjAwMSAxMzcuNUMwLjAwMSAxNDQuNDA0IDUuNTk3IDE1MCAxMi41MDEgMTUwSDc1LjQyMkw5LjA5NCAxOTMuMjMzQzMuNjE5IDE5Ni44MDIgMCAyMDIuOTc4IDAgMjEwQzAgMjIxLjA0NiA4Ljk1NCAyMzAgMjAgMjMwQzI3LjAyMiAyMzAgMzMuMTk4IDIyNi4zOCAzNi43NjYgMjIwLjkwNkw4MC4wMDEgMTU0LjU3OVYyMTcuNUM4MC4wMDEgMjI0LjQwNCA4NS41OTcgMjMwIDkyLjUwMSAyMzBDOTkuNDA1IDIzMCAxMDUuMDAxIDIyNC40MDQgMTA1LjAwMSAyMTcuNVYxMjVIMTIuNTAxWiIgZmlsbD0iI0VBM0I5QyIvPgo8cGF0aCBkPSJNMTc3LjUgMTIwQzE0OC41MDUgMTIwIDEyNSAxNDMuNTA1IDEyNSAxNzIuNVYyMjVIMTc3LjVDMjA2LjQ5NSAyMjUgMjMwIDIwMS40OTUgMjMwIDE3Mi41QzIzMCAxNDMuNTA1IDIwNi40OTUgMTIwIDE3Ny41IDEyMFoiIGZpbGw9IiNGNEI2MzUiLz4KPGRlZnM+CjxjbGlwUGF0aCBpZD0iY2xpcDBfMTFfNDU2Ij4KPHJlY3Qgd2lkdGg9IjExMCIgaGVpZ2h0PSIxMTAiIGZpbGw9IndoaXRlIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMjApIi8+CjwvY2xpcFBhdGg+CjwvZGVmcz4KPC9zdmc+Cg==&query=download_count&suffix=%20Downloads&label=Marketplace&labelColor=151515&color=204cfe&url=https://mp-gateway.elgato.com/organizations/4f6509ec-dafb-4b1f-8b99-e00aa7f80e79/products/1466943f-b058-4e6c-be04-cbd65ce09b31 "Marketplace download badge")](https://marketplace.elgato.com/product/window-actions-1466943f-b058-4e6c-be04-cbd65ce09b31)

This plugin allows a user to manipulate windows on Windows 10+, with the tap of a button or through a multi-action sequence, while using an [Elgato Stream Deck](https://www.elgato.com/en/stream-deck)

<br/>
<a href="https://www.buymeacoffee.com/arkyasmal" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

# Quickstart

Download the following [setup file](https://github.com/aasmal97/Window-Actions/releases/tag/v4.2.0)

### Pre-requisites

- StreamDeck 4.1 +
- Windows 10+

# Description

The Elgato Stream Deck natively supports a [open system action](https://help.elgato.com/hc/en-us/articles/360028234471-Elgato-Stream-Deck-System-Actions-Hotkey-Open-Website-Multimedia-#h_01G93K00TJB5BHV93JTTJ0YV80), which can be used to open any application you need. However, it lacks the ability to perform window actions of the windows that this action creates. When setting up a multi-action workflow, streaming, or recording, these actions are almost essential to have, since multiple applications need to be hidden or focused in.

This app allows users to use an Elgato Stream Deck to minimize, close, maximize, resize, focus or move windows on a Windows 10+ machine. It also supports Virtual Desktops and allows for their creation and navigation

# Alternative Workaround

On a Windows 10+ machine, a workaround to perform these window actions (minimize, close, maximize, resize or move), would be to download [`nircmd`](https://www.nirsoft.net/utils/nircmd.html), and create a `.bat` file, that when opened, runs a series of commands to perform such actions. However, this comes with the following problems:

1. It's tedious to configure a different `.bat` file for every window action needed
2. This requires learning the Windows OS CLI (Command Prompt or Powershell).
3. It's difficult to change the workflow in the future, as it requires manually updating a new [window identifier](#window-identifiers) in the `.bat` file directly. This may be necessary if an application updates itself and it's identifiers change, or if an action was configured for a one-time use case using `hwid`.
4. `nircmd` does not support virtual desktops (moving or navigating through them)
5. `nircmd` is over decade old, and is potentially outdated and includes secruity vulnerabilities

   To amend these problems, this app/plugin was developed

# How This Plugin Works

### General Architecture

![alt Window actions General Architecture Layout](./window-actions-architecture.png)

### Initiating Window Action Commands

 This app uses the [Win32 API](https://learn.microsoft.com/en-us/windows/win32/apiindex/windows-api-list) to initiate most window actions. We use python's [pywin32 library](https://pypi.org/project/pywin32/) to wrap around this API, and expose their actions to us. 

### Initiating Monitor/Virtual Desktop Commands

To initiate virtual desktop and monitor actions, like moving a window to another virtual desktop or monitor, we send commands to a specific version of `VirtualDesktopAccessor.dll`. The multiple dll versions are [stored here](./Sources/com.arkyasmal.windowActions.sdPlugin/app/dll). 

Documentation for these files can be [found here](https://github.com/Ciantic/VirtualDesktopAccessor)

Ultimately, This allows us to interact with the Windows 10 and 11 unoffical Virtual Desktop API. We then package these dll files with the app.
### Integrating Our App

We integrate our app with the [Elgato Stream Deck Architecture](https://docs.elgato.com/sdk/plugins/architecture) by compiling our python app into an `.exe` file, using [cx_Freeze](https://cx-freeze.readthedocs.io/en/stable/index.html). This `.exe` file becomes the entry point/Code path that our `manifest.json` points to for the plugin.

### Configuring the Property Inspector

This is where most of the magic happens. Using Elgato's Property Inspector, we can create a simple and initutive HTML form, that accepts the required [window Identifier](#window-identifiers), and passes it into our plugin, to execute. The quickest way to set this up, is by using pre-populated dropdowns, that can be selected. This prevents typos, and incorrect mappings, which commonly occur when writing directly to `.bat` files.

As an added bonus, it also means users don't need to write any code to configure their actions.

### Populating Active Window Dropdown

To automatically populate a dropdown list of active/opened windows, we use pywin32's [`win32gui`](https://pypi.org/project/win32gui/#description) module. The result is then passed to the [property inspector](#configuring-the-property-inspector), for user selection.

# Window Identifiers

The following are the valid identifier types that can be configured.

- program name/process (.exe file name)
- window title (partial or exact)
- [window handle](https://learn.microsoft.com/en-us/windows/apps/develop/ui-input/retrieve-hwnd) (`hwnd`)
- [window class name](https://learn.microsoft.com/en-us/windows/win32/winmsg/about-window-classes).

# For users still on Version 3 or below, on the plugin:

When the plugin was initially concieved, it relied on reputable third-party executables to interact with the OS. However, after version 3, I made the decision to eliminate as many dependencies as possible, and rewrote the functions of these third-party executables, directly into the plugin code. This eliminated the need for these third parties, and reduced the size of the plugin. HOWEVER, this also potentially caused errors with updating the plugin.

If you want to update the plugin to its most recent version (v4) PLEASE FOLLOW the video below :) !

https://github-production-user-asset-6210df.s3.amazonaws.com/74555081/380882151-1fc88f8e-4b40-4c17-99aa-24daa5bf083c.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250411%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250411T134000Z&X-Amz-Expires=300&X-Amz-Signature=ea0c7f096ab18d798c0564d1c8b72b04909188113be46cca48ee53302ee95fb5&X-Amz-SignedHeaders=host

