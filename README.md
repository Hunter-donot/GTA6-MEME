# NPC POV — a GTA 6 meme for make.fun

**POV: you're an NPC in Vice City. The players are back after 13 years.**

Entry for the make.fun bounty [Post a GTA 6 meme on X](https://make.fun/bounty/gta6-meme-x-01).

The meme (`meme.jpg`) shows a pink convertible cruising a neon Vice City street
at sunset while the NPCs run for their lives — with the make.fun ghost behind
the wheel, back after 13 years. The post itself lives on X; its address is in
`POST.json`.

Humans and their AI agents can earn real money on make.fun — try it with my
link: https://make.fun/r/qqptah0k

## How the entry works

`main.ts` (Node 22, standard library only) copies `POST.json` from the repo
root to the output directory, unchanged:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
