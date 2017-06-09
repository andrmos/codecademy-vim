# codecademy-vim
Vim (Neovim) integration with Codecademy.

*Disclaimer: This is a proof of concept/work in progress, created with no prior experience with python or plugin development for Vim.
The code is therefore subpar, and might not work properly.*

## Aim
The aim is to be able to solve Codecademy programming lessons in Vim, with all Vim mappings and commands you are used to.
- Enter code from Vim into the Codecademy web editor with a Vim command
- Pull code from the web editor into Vim with a Vim command
- Run the code in the web editor with a Vim command
- Navigate different Codecademy lessons with Vim commands
- ...

## Progress
- [x] Automatically log into Codecademy on startup
- [x] Enter code into the web editor with mapping `<Leader>cs`
- [x] Pull code into from the web editor into Vim with mapping `<Leader>cg`
- [x] Run the code in the web editor with mapping `<Leader>cr`
- [ ] Improve documentation and how to use
- [ ] Support *normal* Vim (currently developed using Neovim)
- [ ] Support other web browsers than Chrome/Chromium
- [ ] Support customisability
- [ ] Improve code structure, error handling and general code quality
- [ ] ...

## Dependencies
- Neovim
- Python3
- Python Selenium
- Chrome/Chromium
- ChromeDriver
- Python-client (python client for Neovim)
