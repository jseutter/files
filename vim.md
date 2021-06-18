# Vim settings

### Indent block/unindent

Set indent size to two with :set ts=2 sw=2.  Then '>' or '<'
on visual block.

### Use spaces instead of tabs
:set ts=4
:set sw=4
:expandtab


### Enable highlighting for mouse copy and paste
:set mouse=r

### Show line numbers
:set number

### Convert DOS to Unix line endings
:set ff? to query
:set ff=unix or dos or mac

### Enable syntax highlighting
:syntax on

### Macro record and use
Record with q<letter><commands>q
Use with <number>@<letter>

A common use is to execute the macro once, then just repeat
the last command with '.'.
