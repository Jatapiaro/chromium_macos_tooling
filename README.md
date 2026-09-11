# Chromium macOS Tooling

I worked in the Chrome a11y team. Building Chromium within the Google infra is
almost a plug-n-play thing.

The main problem is that, Chromium source code requires a lot of storage, plus
each build requires even more storage depending on what you build and how you
build it.

The motivation is that, I got rid of a fast MacBook Pro and moved to a MacBook 
Neo that is just a fancy client that connects to my beffy PC at Home.

Keeping the idea of compiling everything on a Linux Machine in the Cloud. Thus
to be able to do that, you need to somehow provide a macOS SDK to keep the 
compilation out of your local machine.

## ToDo

- Add an rsync utility: Compile fast in the cloud, run local.
- Add a way to provide arguments for the generate_sdk script