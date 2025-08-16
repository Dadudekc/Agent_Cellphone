# 🌙 Overnight Digest — {{date}}
- Tasks processed: {{count}}
- Stale agents: {{stale}}
## Task Outcomes
{{#each tasks}}
- {{status}} **{{id}}**: {{from}} → {{to}} ({{checks}} checks)
{{/each}}
## Agent Heartbeats
{{#each heartbeats}}
- {{icon}} {{agent}}: {{msg}}
{{/each}}
