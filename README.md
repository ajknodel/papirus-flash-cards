# papirus-flash-cards
The bulk of the python code used to create a flash card device using a Raspberry Pi and e-ink display


## Flashcards with Raspberry Pi Papirus e-ink display
This code was written to help me learn a new language (Korean). It uses an Anki database and the Anki-Connect Add-on API to randomly select a card out of all decks except the "Default" deck, which I use to archive old cards instead of delete them.

Anki: https://apps.ankiweb.net/
Anki-Connect API: https://github.com/FooSoft/anki-connect
Papirus e-ink display: https://uk.pi-supply.com/products/papirus-epaper-eink-screen-hat-for-raspberry-pi

'refresh.py' runs on a cron job every minute and gives me a new card from Anki running on a VM nearby.

'buttons' is the program that runs in the background to listen for button events.

Button 4 moves a card that I have effectively memorized to the Default deck so I don't see it again and then gives me a new card

Button 3 moves to the next random card in line

Button 2+1 pressed together turns off the Raspberry Pi so it can be moved, unplugged, etc. safely.

This project started just because I was looking for something to do with both a Raspberry Pi and an e-ink display. This has been a good application and helped me learn many words more passively. It sits under my computer monitor and I glance down occassionally to remind myself of some words, phrases, or grammar points that I am studying.

Anki was used because it syncs with my phone, so I can keep an up-to-date list of cards to study and study them both on the pi and on my phone.