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
Repeat last macro with @@

If you find macro repetition problematic, :map , @@ to make
the comma key act like '.'.

### Taking notes
Use vim-notes plugin, configured with Vundle

### Navigating
Move forward to another file with 'gf'
Go back with Ctrl-6, or Ctrl-O Ctrl-O

Move between screens with Ctrl-w, followed by an arrow key

### Package Management
Use Vundle - Directions on Internet, but start with modifying .vimrc
