# materials — site

Public repository of the materials site: <https://d1-d57.github.io/materials/>.

Only the site lives here: Hugo sources (`content/`, `data/`, `layouts/`, `static/`, `hugo.yaml`) and the Pages workflow `.github/workflows/hugo.yml`, which builds and publishes on every push to `main`. Hugo version is pinned in the workflow.

Courses, the problem base and lessons with pupils live in private repositories; the old monorepo is the private archive `arhiv-materials`.

Build locally: `hugo server` (Hugo extended, same version as in the workflow).
