# New Year's Fireworks Simulator in your Terminal

At your desk for New Years? Crack open a beer and a terminal. Run this app, and wait for the fireworks!


Pythonistas, run the following (requires [uv](https://docs.astral.sh/uv/getting-started/installation/)):

```
uvx ny2026@latest
```

JS fans, run the following:

``` 
npx @manzt/uv tool run ny2026
```

You can also press SPACE if you are impatient for the fireworks to start...

<img alt="Screenshot 2025-12-28 at 21 42 21" src="https://github.com/user-attachments/assets/f9872cec-27a6-4154-b481-ee9383c8e46e" />



## How this was built

This project was built with [Toad](https://github.com/batrachianai/toad) and [Claude Code](https://code.claude.com/docs/en/overview).

It was an excercise in "vibe coding". Something I hadn't done a great deal of.

Could I have done this "by hand"? Yeah, probably. I am an ex game developer and I work with terminals. Claude one-shotted much of this. But it did create bugs that it couldn't fix, and I had to use my fleshy mammalian brain to resolve. It really struggled with the audio. There were many rounds of "I see the problem! There it is fixed now", but it did eventually get there.

There was also a last minute bug reported by another mamallian brain. It was using UTC for the countdown, which would have made it wrong for anyhone outside the UK.

Of course I should have checked, but I kind of feel that a human would be less likely to make that mistake. If you actually had to type UTC in the code, that should have triggered the realization that it would break for other timezones.

Overall, the coad is not bad. Not good, but not terrible. There are some lines which I don't think are even neccesary. Reminants of failed experiments perhaps. I suspect Claude could easily tidy those up, but you do need to know to ask.

Considering there isn't a large corpus of firework simulations with braille characters in the terminal (I assume), I think Claude did OK here.

Anyhow. These videos represent a snapshot of the process.

https://github.com/user-attachments/assets/165d8aca-2f2f-4bfd-802d-5f8c33b0d0c3

https://github.com/user-attachments/assets/4a69c8ef-676d-487f-92c9-556ae907d4d9
