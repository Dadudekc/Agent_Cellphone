# Agent Onboarding Checklist

- [ ] Read and understand `UPDATE_STATUS_GUIDE.md` (status protocol is mandatory)
- [ ] Implement the `update_status` helper in your agent code
- [ ] Update `status.json` after **every** action, state change, or message
- [ ] Always set a clear `message` for the user when waiting, busy, or on error
- [ ] Test your status reporting in the Dream.OS UI (refresh to verify)
- [ ] Keep your workspace clean and up-to-date (remove old logs, temp files)
- [ ] Review `AGENT_TRAINING_GUIDE.md` and `ONBOARDING_SUMMARY.md` for full protocol 