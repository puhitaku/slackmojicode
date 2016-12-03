# SlackMojicode

**Programming emoji interpreter works on Slack as a bot.**

This language is based on joshsharp's Braid.

Tokens are replaced with emoji-style one as you see in below picture, and you can find assinments [here](slackmojicode/lexer.py).

![Run script](pic/run.png)
![Convert script](pic/convert.png)

## Installing

`pip install -r requirements.txt`

Add your Slack bot's token in `rtmbot.conf` then execute `rtmbot` .

## Running

`python braid.py` for REPL, `python braid.py [filename].bd` for interpreting a file

`:a` gives you the AST of the last statement, `:e` to list environment variables, `:q` or Ctrl-C to quit. The REPL now supports multi-line input too — it'll just keep appending code and trying to interpret it until it's valid (eg. you closed the block or whatever), or you break it ;)

## Modification

Some modifications from Braid was applied:

 - Non-immutable variable (re-assignable)
 - Re-implemented print function
 - Decreased / replaced tokens

