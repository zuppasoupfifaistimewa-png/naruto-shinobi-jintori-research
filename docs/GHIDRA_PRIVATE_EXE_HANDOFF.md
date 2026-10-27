# Private handoff for Ghidra analysis of SLPS_035.53

## Purpose and current state

Workflow: [Ghidra static analysis — SLPS_035.53](../.github/workflows/ghidra-static-analyze-psx-exe.yml).

Ghidra 12.2 setup has already been verified in Actions run [#40434733043](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40434733043). This workflow is the next stage: securely download the main PS-X EXE, validate it, run the reproducible RNG-signature scan, run Ghidra headless, and export a **text-only function index**. The workflow does not launch the game or an emulator.

The runner needs a direct-download URL configured by the repository owner. The ChatGPT/GitHub connector cannot create repository Actions secrets or transfer the private Library binary directly to a runner, so the analysis cannot start until this one-time configuration is done.

## Required secret

Create a **repository Actions secret** named:

- `PSX_EXE_DOWNLOAD_URL` — an HTTPS URL that serves the exact binary `SLPS_035.53` as a direct download. The secret must remain valid when the workflow runs.

On GitHub, open this repository, then **Settings → Secrets and variables → Actions → New repository secret**. Enter the name exactly as above and put the URL only in the secret value.

Use a private file host or a private storage object with access-controlled HTTPS download. A short-lived signed URL is acceptable only while it remains valid; rotate the secret if it expires. Do not paste the URL in a chat, issue, commit, workflow input, or log. Do not make the executable public merely to automate analysis.

## Validation performed by the workflow

The downloaded file is rejected and deleted unless all checks pass:

- File name used locally: `SLPS_035.53`
- Exact size: `385024` bytes
- PS-X EXE magic: `PS-X EXE`
- Expected SHA-256: `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`

These are the executable values recorded in the existing local-header verification. The workflow does not trust the URL alone.

## Run the analysis

After the secret is configured:

1. Open the repository **Actions** tab.
2. Select **Ghidra static analysis — SLPS_035.53**.
3. Choose **Run workflow** on branch `main`.

Expected text-only artifact: `ghidra-slps-03553-function-index`, retained for 14 days. It contains the function TSV, the RNG-signature scan/caller list, analysis configuration, validation report, and text logs. It never includes the executable or Ghidra project. The workflow deletes the private input and temporary Ghidra project before the runner exits.

## Boundaries

- Only static analysis of `SLPS_035.53`; no emulator, gameplay, ROM, BIOS, savestate, Memory Card or screenshot is run/uploaded.
- The function TSV is an initial index, not proof that a candidate function controls RNG, Chakra transactions, roulette, barrier selection or victory rules.
- The binary is never added to Git or to the Actions artifact.
- The independent adaptive-player gates remain unchanged: cue UNKNOWN, `barrier_level_selection = WAIT`, readiness NO-GO, Story Mode NOT COMPLETE; Revision65 remains untouched.
