# TODO_ADMIN_TASK.md

## Goal
Admin register page + admin dashboard click-to-view student details.

## Steps
- [ ] Create admin-details view route that fetches students by `registers.email` and shows `raja` fields.
- [ ] Update `init_db()` (if needed) to ensure columns exist for joining.
- [ ] Update `/details` route to store `email` consistently (already exists) and optionally store `username` in `raja`.
- [ ] Update `admin_dashboard.html` to make student name clickable and link to details view.
- [ ] Enable admin registration by removing disabled button and removing "registration disabled" behavior.
- [ ] Keep other features unchanged.
- [ ] Quick test: admin login, open dashboard, click student, ensure details appear.

