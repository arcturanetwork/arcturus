---
title: "Arcturus | Arctura Network's Reference Implementation"
meta_description: "Arcturus is Arctura Network's reference implementation, running on Bittensor testnet under netuid 505. The code behind the Work Standard, in the open."
target_keyword: "Arctura Bittensor subnet implementation open source"
url: "https://github.com/arcturanetwork/arcturus"
canonical: "https://github.com/arcturanetwork/arcturus"
og_title: "Arcturus | Arctura Network's Reference Implementation"
og_description: "The code behind Arctura Network's Work Standard, running live on Bittensor testnet under netuid 505."
og_type: "website"
twitter_card: "summary_large_image"
robots: "index,follow"
status: "draft — not yet passed Council review"
lastmod: "PENDING — set on publish"
image:
  filename: "arcturus-repo-social-card.webp"
  format: webp
  alt_text: "Arcturus repository banner — Arctura Network's reference implementation on Bittensor testnet netuid 505"
---

# Arcturus

Arctura Network's reference implementation. This is the code that runs the Work Standard — not a description of it.

**Status:** Live on Bittensor testnet, netuid 505. No mainnet netuid published yet.

---

## What this is

Arcturus is where Arctura's rules stop being written and start being run. Every part of the [Work Standard](https://arctura.network/work-standard/) — checkable work, bounded decisions, an honest record — is implemented here as running code, not just described on the site.

If you want to read the standard, go to [arctura.network/work-standard](https://arctura.network/work-standard/). If you want to see it enforced, this is that.

## What it does

- Runs as a subnet on Bittensor testnet under **netuid 505**
- Accepts and checks contributed work against the network's review process
- Keeps a public, checkable record of what was submitted, reviewed, and accepted
- Applies the Council's five checks — Need, Clarity, Usefulness, Durability, Reversal — to proposed changes before they're accepted

## What it doesn't do (yet)

- No mainnet deployment. Testnet only.
- [Confirm: does it currently handle payment/value transfer, or is that still separate? — flag before publish]
- [Confirm: current test coverage / audit status before this claims production-readiness]

## Getting started

```bash
git clone https://github.com/arcturanetwork/arcturus.git
cd arcturus
# [setup steps — confirm actual install/run commands before publish]
```

Full setup and node-operation steps: see [Documentation](https://arctura.network/documentation/netuid-505/).

## Verify it yourself

Nothing here asks to be taken on faith.

- Commit history is public in this repo.
- Testnet activity under netuid 505 is checkable against [Evidence](https://arctura.network/evidence/netuid-505/).
- Every accepted change went through the same five checks described in [Authority](https://arctura.network/authority/).

## Contributing

Contributions are reviewed against the [Work Standard](https://arctura.network/work-standard/), not just for code quality. A pull request is a proposed change — it goes through the same checks as any other change to the network.

[Confirm: contribution process, issue template, license before publish]

## License

[Confirm license before publish — currently unspecified]

---

*Maintained by Arctura Network. Part of the same public record described at [arctura.network](https://arctura.network/).*
