# OS X Settings

## Citrix client key repeating doesn't work

OS X has a feature where when you hold down a key like h,j,k,l, it
brings up a menu with diacritics for that letter.  This intercepts
keyboard events when you are trying to use Vim in a Citrix virtual
desktop session.  The symptom is that your Citrix will beep at you
whenever you hold a key down.

The fix is to disable this popup menu using the command:

defaults write -g ApplePressAndHoldEnabled -bool false

This setting won't take effect until you log out and back in to
OS X.

## xcrun error when running git

OS X updated and broke everything like usual:
xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun

Run `xcode-select --install` to fix.

