# Unitask Agent Use Cases (Compact)

Use these prompts to get fast value from `unitask-agent`.

## Plan Day
1. "What are my todo tasks right now?"
   - Tool path: `list_tasks(status=todo)`
2. "Show only parent tasks I should focus on first."
   - Tool path: `list_tasks(status=todo,parent_id=null)`
3. "Show subtasks under this parent: <parent_id>."
   - Tool path: `list_tasks(parent_id=<id>)`
4. "Build a 9-5 plan and preview it first."
   - Tool path: `plan_day_timeblocks(apply=false)`
5. "Apply the exact plan you just previewed."
   - Tool path: `plan_day_timeblocks(apply=true)`

## Capture
6. "Create a task: finalize launch copy."
   - Tool path: `create_task`
7. "Create a subtask under <parent_id>: draft FAQ."
   - Tool path: `create_task(parent_id)`
8. "Create this task with high priority and due date tomorrow."
   - Tool path: `create_task(priority,due_date)`
9. "Add a recurring task every weekday."
   - Tool path: `create_task(recurrence)`
10. "Convert this note into a task and schedule 45 minutes tomorrow 10am."
   - Tool path: `create_task(scheduled_start,duration_minutes)`

## Organize
11. "Rename task <id> to clearer action language."
   - Tool path: `update_task(title)`
12. "Set task <id> priority to critical and add context in description."
   - Tool path: `update_task(priority,description)`
13. "Move subtask <task_id> from parent A to parent B (preview first)."
   - Tool path: `move_subtask(dry_run=true)`
14. "Now apply that subtask move."
   - Tool path: `move_subtask(dry_run=false)`
15. "Merge parent B into parent A with all subtasks, preview first."
   - Tool path: `merge_parent_tasks(dry_run=true)`
16. "Apply that parent merge now."
   - Tool path: `merge_parent_tasks(dry_run=false)`
17. "List all tasks tagged urgent."
   - Tool path: `list_tasks(tag_id=<tag_id>)`
18. "Create tags: urgent, deep-work, admin."
   - Tool path: `create_tag`
19. "Attach tag <tag_id> to task <task_id>."
   - Tool path: `add_task_tag`
20. "Remove tag <tag_id> from task <task_id>."
   - Tool path: `remove_task_tag`

## Cleanup
21. "Mark task <id> done."
   - Tool path: `update_task_status(status=done)`
22. "Reopen task <id> back to todo."
   - Tool path: `update_task_status(status=todo)`
23. "Soft-delete this obsolete task tree: <id>."
   - Tool path: `delete_task`
24. "Soft-delete outdated tag <id>."
   - Tool path: `delete_tag`

## Review
25. "Show me my settings and suggest optimizations for speed and focus."
   - Tool path: `get_settings` + `update_settings`
26. "Update my onboarding preferences based on my role and work style."
   - Tool path: `update_settings(quiz)`
27. "Estimate where my day is overloaded from current scheduled blocks."
   - Tool path: `list_tasks` + `plan_day_timeblocks(apply=false)`

## Safety Defaults
- Use dry-run first for `move_subtask` and `merge_parent_tasks`.
- Confirm destructive actions before applying `delete_task` or `delete_tag`.
- Use least-privilege token scopes (`read`, `write`, `delete`) for each workflow.
