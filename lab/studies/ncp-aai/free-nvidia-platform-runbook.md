# Free NVIDIA platform lab runbook

**Verified:** 2026-09-03 against NVIDIA's current Agent Toolkit 1.8, NeMo
Guardrails, and NIM API documentation. Recheck the linked pages before running:
package extras, available models, quotas, and account terms can change.

This is an original, evidence-oriented replacement for unverified setup snippets in
community study guides. It covers hosted NIM inference, NeMo Agent Toolkit (NAT),
and NeMo Guardrails. It does **not** claim that hosted inference is permanently or
unconditionally free.

## Boundaries and prerequisites

- An NVIDIA account and a personal key created at [build.nvidia.com](https://build.nvidia.com/) are required for hosted NIM calls.
- Never paste a key into source, shell history, screenshots, transcripts, or evidence. Never run `echo $NVIDIA_API_KEY`.
- Hosted inference at `integrate.api.nvidia.com` is different from self-hosting a NIM container. The latter can require Docker, compatible NVIDIA hardware/software, image access, and an entitlement.
- NAT itself and NeMo Guardrails can run without a local GPU; the selected model provider may be remote.
- Use an isolated Python 3.11–3.13 virtual environment. Record exact package versions in the evidence.

No account was created and no credentialed request was made while authoring this
runbook. Those actions require the learner's account and key.

## 1. Load the key without displaying it

Start a fresh shell whose history will not contain the secret, read it silently,
and export it only to child processes:

```bash
read -rsp "NVIDIA API key: " NVIDIA_API_KEY
export NVIDIA_API_KEY
printf '\nKey loaded (value not displayed).\n'
```

Do not use shell tracing (`set -x`). At the end of the session run
`unset NVIDIA_API_KEY`. If a key appears in a log or commit, revoke it and create a
replacement; redaction alone does not undo exposure.

## 2. Hosted NIM smoke test

Choose an available model on build.nvidia.com and copy its current model ID. The
official LLM API is a bearer-authenticated `POST` to
`https://integrate.api.nvidia.com/v1/chat/completions`. The following deliberately
uses a placeholder so a stale model is not silently selected:

```bash
export NVIDIA_MODEL_ID='<current-model-id-from-build.nvidia.com>'
curl -sS https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer ${NVIDIA_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d "{\"model\":\"${NVIDIA_MODEL_ID}\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with exactly: platform-smoke-ok\"}],\"temperature\":0,\"max_tokens\":16}"
```

Pass only if the HTTP request succeeds, the response is valid JSON, and the answer
matches the requested phrase. Save a redacted record containing timestamp, endpoint,
model ID, HTTP status, request ID if returned, latency, and output—never headers or
the key. A 401/403, quota error, or unavailable model is a failed/blocked run, not a
pass.

## 3. Install and verify NeMo Agent Toolkit 1.8

The current official package install is recommended for production use. Source
installation is required for checked-in examples.

```bash
python3 -m venv .venv-nat
source .venv-nat/bin/activate
python -m pip install --upgrade pip
python -m pip install nvidia-nat
nat --version
nat --help
python -m pip freeze
```

Install only the plugins a lab needs. Current documented extras include:

```bash
python -m pip install 'nvidia-nat[langchain]'
python -m pip install 'nvidia-nat[eval]'
python -m pip install 'nvidia-nat[profiler]'
python -m pip install 'nvidia-nat[security]'
python -m pip install 'nvidia-nat[guardrails]'
```

Do not copy the older `profiling` extra into a 1.8 environment. Confirm conflicts
and optional dependencies in the current install guide before combining extras.
For each NAT exercise, capture configuration, sanitized inputs/outputs, tool calls,
trace IDs, evaluator results, version freeze, and a failure-path test. Merely seeing
`nat --help` proves installation, not agent competence.

## 4. Install and verify NeMo Guardrails

The official quick start installs the independent package with pip. Its library can
run on CPU; NVIDIA-hosted tutorial models still require the key.

```bash
python3 -m venv .venv-rails
source .venv-rails/bin/activate
python -m pip install --upgrade pip
python -m pip install nemoguardrails
nemoguardrails --help
python -m pip freeze
```

Build one allow case and at least four denial/adversarial cases: prompt injection,
PII exfiltration, prohibited tool use, and unsafe output. A pass requires expected
policy decisions, no unauthorized side effect, and an audit record that explains
which rail fired. Test fail-closed behavior when the safety model or provider is
unavailable.

## 5. Evidence and cleanup gate

A platform lab is complete only when its evidence contains:

1. UTC timestamp, machine/runtime description, and exact package versions.
2. Sanitized command/configuration and immutable source/version identifiers.
3. Expected result, observed result, latency, and pass/fail decision.
4. At least one injected failure and its recovery or fail-closed behavior.
5. Confirmation that secret scanning found no key material.

Then unset the key, deactivate the environment, and revoke disposable keys in the
NVIDIA account. Do not commit virtual environments or raw provider responses.

## Official references

- [NAT 1.8 installation](https://docs.nvidia.com/nemo/agent-toolkit/latest/quick-start/installing.html)
- [NAT overview and NIM example](https://docs.nvidia.com/nemo/agent-toolkit/latest/index.html)
- [NeMo Guardrails installation](https://docs.nvidia.com/nemo/guardrails/get-started/installation-guide)
- [NVIDIA LLM NIM API](https://docs.api.nvidia.com/nim/reference/llm-apis)

