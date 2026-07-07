#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/custom-license-policy.sh"

OWNER=""
REPO_NAME=""
DESCRIPTION=""
VISIBILITY="public"
TARGET_DIR=""
DEFAULT_BRANCH="main"
DRY_RUN=1

COMMIT_MESSAGE="chore: apply custom license policy (attribution + NC + state-school only)"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/create-repo-with-custom-license.sh [options]

Options:
  --owner <owner>               GitHub user/org owner (required)
  --name <repo-name>            New repository name (required)
  --description <text>          Repository description
  --visibility <public|private> Visibility (default: public)
  --target-dir <path>           Parent directory for clone (default: current dir)
  --default-branch <name>       Preferred default branch for first push (default: main)
  --apply                       Create/push repository and apply license files
  --dry-run                     Show what would happen (default)
  --help                        Show this help

Examples:
  bash scripts/create-repo-with-custom-license.sh \
    --owner ChristineJanischek \
    --name mein-neues-repo \
    --description "Neues Projekt" \
    --dry-run

  bash scripts/create-repo-with-custom-license.sh \
    --owner ChristineJanischek \
    --name mein-neues-repo \
    --description "Neues Projekt" \
    --visibility public \
    --apply
EOF
}

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[repo-license-bootstrap] ERROR: required command not found: $cmd" >&2
    exit 1
  fi
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --owner)
        OWNER="${2:-}"
        shift 2
        ;;
      --name)
        REPO_NAME="${2:-}"
        shift 2
        ;;
      --description)
        DESCRIPTION="${2:-}"
        shift 2
        ;;
      --visibility)
        VISIBILITY="${2:-}"
        shift 2
        ;;
      --target-dir)
        TARGET_DIR="${2:-}"
        shift 2
        ;;
      --default-branch)
        DEFAULT_BRANCH="${2:-}"
        shift 2
        ;;
      --apply)
        DRY_RUN=0
        shift
        ;;
      --dry-run)
        DRY_RUN=1
        shift
        ;;
      --help|-h)
        usage
        exit 0
        ;;
      *)
        echo "[repo-license-bootstrap] ERROR: unknown option: $1" >&2
        usage
        exit 1
        ;;
    esac
  done
}

validate_args() {
  if [[ -z "$OWNER" ]]; then
    echo "[repo-license-bootstrap] ERROR: --owner is required" >&2
    exit 1
  fi

  if [[ -z "$REPO_NAME" ]]; then
    echo "[repo-license-bootstrap] ERROR: --name is required" >&2
    exit 1
  fi

  if [[ "$VISIBILITY" != "public" && "$VISIBILITY" != "private" ]]; then
    echo "[repo-license-bootstrap] ERROR: --visibility must be public or private" >&2
    exit 1
  fi
}

main() {
  parse_args "$@"
  require_cmd gh
  require_cmd git
  validate_args

  local full_repo="$OWNER/$REPO_NAME"
  local work_parent="${TARGET_DIR:-$PWD}"
  local repo_dir="$work_parent/$REPO_NAME"

  echo "[repo-license-bootstrap] repo=$full_repo visibility=$VISIBILITY dry_run=$DRY_RUN"
  echo "[repo-license-bootstrap] target_dir=$repo_dir"

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[repo-license-bootstrap] DRY-RUN would execute:"
    echo "  1) gh repo create $full_repo --$VISIBILITY --clone --add-readme"
    echo "  2) apply custom LICENSE/NOTICE/README marker block"
    echo "  3) git commit + git push"
    exit 0
  fi

  mkdir -p "$work_parent"

  if [[ -d "$repo_dir/.git" ]]; then
    echo "[repo-license-bootstrap] ERROR: target repo directory already exists: $repo_dir" >&2
    exit 1
  fi

  local visibility_flag="--public"
  if [[ "$VISIBILITY" == "private" ]]; then
    visibility_flag="--private"
  fi

  local create_args=(repo create "$full_repo" "$visibility_flag" --clone --add-readme)
  if [[ -n "$DESCRIPTION" ]]; then
    create_args+=(--description "$DESCRIPTION")
  fi

  (
    cd "$work_parent"
    gh "${create_args[@]}"
  )

  if [[ ! -d "$repo_dir/.git" ]]; then
    echo "[repo-license-bootstrap] ERROR: clone failed or repo directory missing: $repo_dir" >&2
    exit 1
  fi

  pushd "$repo_dir" >/dev/null

  local current_branch
  current_branch="$(git symbolic-ref --short HEAD 2>/dev/null || true)"
  if [[ -z "$current_branch" ]]; then
    current_branch="$DEFAULT_BRANCH"
    git checkout -B "$current_branch"
  fi

  if [[ "$current_branch" != "$DEFAULT_BRANCH" ]]; then
    git branch -m "$DEFAULT_BRANCH"
    current_branch="$DEFAULT_BRANCH"
  fi

  apply_custom_license_policy "$repo_dir"

  git add LICENSE NOTICE README.md 2>/dev/null || git add LICENSE NOTICE

  if git diff --cached --quiet; then
    echo "[repo-license-bootstrap] SKIP unchanged: no license changes to commit"
    popd >/dev/null
    exit 0
  fi

  git commit -m "$COMMIT_MESSAGE"
  git push -u origin "$current_branch"

  echo "[repo-license-bootstrap] DONE: custom license policy applied to $full_repo"
  popd >/dev/null
}

main "$@"