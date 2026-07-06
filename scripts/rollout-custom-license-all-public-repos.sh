#!/usr/bin/env bash
set -euo pipefail

# Roll out a custom license policy to all public repositories of an owner.
# Policy summary:
# - Attribution required
# - Non-commercial only
# - Use only in state school contexts
# - Any other use requires explicit permission

OWNER=""
BRANCH_NAME="chore/custom-license-cj-nc-school"
COMMIT_MESSAGE="chore: apply custom license policy (attribution + NC + state-school only)"
PR_TITLE="Apply custom license policy (Attribution + NC + state-school only)"
PR_BODY="This PR applies a repository-wide custom license policy.

Allowed without separate permission:
- Attribution is mandatory
- Non-commercial use only
- Use only in state school contexts

Any other use requires explicit written permission from the rights holder.
"
BASE_BRANCH=""
WORK_DIR=""
INCLUDE_REPOS=""
EXCLUDE_REPOS=""
CREATE_PR=0
PUSH_CHANGES=0
DRY_RUN=1

usage() {
  cat <<'EOF'
Usage:
  bash scripts/rollout-custom-license-all-public-repos.sh [options]

Options:
  --owner <owner>                 GitHub user/org owner (required)
  --base-branch <branch>          Base branch for PRs and resets (default: repo default branch)
  --branch-name <name>            Branch name for license changes
  --work-dir <path>               Working directory for temporary clones
  --include "repo1,repo2"         Only process these repository names (no owner prefix)
  --exclude "repo3,repo4"         Skip these repository names (no owner prefix)
  --push                          Push branch to origin
  --create-pr                     Create PR after push
  --apply                         Apply changes (default is dry-run)
  --dry-run                       Explicit dry-run mode
  --help                          Show this help

Examples:
  bash scripts/rollout-custom-license-all-public-repos.sh --owner ChristineJanischek --dry-run

  bash scripts/rollout-custom-license-all-public-repos.sh \
    --owner ChristineJanischek \
    --push --create-pr --apply
EOF
}

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[license-rollout] ERROR: required command not found: $cmd" >&2
    exit 1
  fi
}

csv_contains() {
  local csv="$1"
  local needle="$2"
  local item

  [[ -z "$csv" ]] && return 1

  IFS=',' read -r -a items <<<"$csv"
  for item in "${items[@]}"; do
    if [[ "${item// /}" == "$needle" ]]; then
      return 0
    fi
  done
  return 1
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --owner)
        OWNER="${2:-}"
        shift 2
        ;;
      --base-branch)
        BASE_BRANCH="${2:-}"
        shift 2
        ;;
      --branch-name)
        BRANCH_NAME="${2:-}"
        shift 2
        ;;
      --work-dir)
        WORK_DIR="${2:-}"
        shift 2
        ;;
      --include)
        INCLUDE_REPOS="${2:-}"
        shift 2
        ;;
      --exclude)
        EXCLUDE_REPOS="${2:-}"
        shift 2
        ;;
      --push)
        PUSH_CHANGES=1
        shift
        ;;
      --create-pr)
        CREATE_PR=1
        shift
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
        echo "[license-rollout] ERROR: unknown option: $1" >&2
        usage
        exit 1
        ;;
    esac
  done
}

write_license_files() {
  local repo_root="$1"

  cat >"$repo_root/LICENSE" <<'EOF'
Custom License - Christine Janischek NC School-Only 1.0

Copyright (c) Christine Janischek
Domain: https://emotionalspirit.de

1. Grant of permission
Subject to all terms below, permission is granted free of charge to use,
copy, adapt, and share this repository and its templates.

2. Mandatory attribution
Any permitted use must provide visible attribution as follows:
"Christine Janischek - https://emotionalspirit.de"

3. Non-commercial restriction
Any commercial use is prohibited.

4. State-school-only restriction
Use is permitted only within the context of state school systems.

5. All other uses require permission
Any use that does not fully satisfy Sections 2-4 is prohibited unless you
obtain explicit prior written permission from the rights holder.

6. No trademark rights
This license does not grant any rights in trademarks, logos, or branding.

7. Disclaimer
THE WORK IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

8. Termination
Any breach of this license terminates your rights under this license
immediately.
EOF

  cat >"$repo_root/NOTICE" <<'EOF'
Attribution Notice

Required attribution text:
Christine Janischek - https://emotionalspirit.de

License policy summary:
- Non-commercial use only
- Use only within state school systems
- All other uses only by explicit prior written permission
EOF
}

ensure_readme_notice() {
  local repo_root="$1"
  local readme="$repo_root/README.md"
  local marker_start="<!-- CUSTOM_LICENSE_NOTICE_START -->"
  local marker_end="<!-- CUSTOM_LICENSE_NOTICE_END -->"

  if [[ ! -f "$readme" ]]; then
    return 0
  fi

  if grep -Fq "$marker_start" "$readme"; then
    awk -v start="$marker_start" -v end="$marker_end" '
      $0==start {
        print
        print "## License"
        print
        print "This repository is licensed under a custom license."
        print ""
        print "- Attribution required: Christine Janischek - https://emotionalspirit.de"
        print "- Non-commercial use only"
        print "- Use only within state school systems"
        print "- Any other use requires explicit prior written permission"
        inblock=1
        next
      }
      $0==end {
        inblock=0
        print
      }
      !inblock { print }
    ' "$readme" >"$readme.tmp"
    mv "$readme.tmp" "$readme"
    return 0
  fi

  cat >>"$readme" <<EOF

$marker_start
## License

This repository is licensed under a custom license.

- Attribution required: Christine Janischek - https://emotionalspirit.de
- Non-commercial use only
- Use only within state school systems
- Any other use requires explicit prior written permission
$marker_end
EOF
}

main() {
  parse_args "$@"

  require_cmd gh
  require_cmd git

  if [[ -z "$OWNER" ]]; then
    echo "[license-rollout] ERROR: --owner is required" >&2
    usage
    exit 1
  fi

  if [[ $CREATE_PR -eq 1 && $PUSH_CHANGES -eq 0 ]]; then
    echo "[license-rollout] ERROR: --create-pr requires --push" >&2
    exit 1
  fi

  if [[ -z "$WORK_DIR" ]]; then
    WORK_DIR="$(mktemp -d)"
  else
    mkdir -p "$WORK_DIR"
  fi

  echo "[license-rollout] owner=$OWNER dry_run=$DRY_RUN push=$PUSH_CHANGES create_pr=$CREATE_PR"
  echo "[license-rollout] work_dir=$WORK_DIR"

  mapfile -t repos < <(gh repo list "$OWNER" --visibility public --limit 1000 --json nameWithOwner,isArchived --jq '.[] | select(.isArchived == false) | .nameWithOwner')

  if [[ ${#repos[@]} -eq 0 ]]; then
    echo "[license-rollout] No public non-archived repositories found for owner: $OWNER"
    exit 0
  fi

  local success_count=0
  local skip_count=0
  local fail_count=0

  for repo_full in "${repos[@]}"; do
    local repo_name="${repo_full#*/}"

    if [[ -n "$INCLUDE_REPOS" ]] && ! csv_contains "$INCLUDE_REPOS" "$repo_name"; then
      echo "[license-rollout] SKIP include-filter: $repo_full"
      skip_count=$((skip_count + 1))
      continue
    fi

    if csv_contains "$EXCLUDE_REPOS" "$repo_name"; then
      echo "[license-rollout] SKIP exclude-filter: $repo_full"
      skip_count=$((skip_count + 1))
      continue
    fi

    echo "[license-rollout] PROCESS $repo_full"

    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[license-rollout] DRY-RUN would update: LICENSE, NOTICE, README.md"
      success_count=$((success_count + 1))
      continue
    fi

    local repo_dir="$WORK_DIR/$repo_name"
    rm -rf "$repo_dir"

    if ! gh repo clone "$repo_full" "$repo_dir" -- -q; then
      echo "[license-rollout] FAIL clone: $repo_full"
      fail_count=$((fail_count + 1))
      continue
    fi

    pushd "$repo_dir" >/dev/null

    local default_branch
    default_branch="$(gh repo view "$repo_full" --json defaultBranchRef --jq '.defaultBranchRef.name')"
    local target_base="${BASE_BRANCH:-$default_branch}"

    git checkout "$target_base" >/dev/null 2>&1 || git checkout -B "$target_base" "origin/$target_base"
    git pull --ff-only origin "$target_base" >/dev/null 2>&1 || true
    git checkout -B "$BRANCH_NAME" >/dev/null 2>&1

    write_license_files "$repo_dir"
    ensure_readme_notice "$repo_dir"

    git add LICENSE NOTICE README.md 2>/dev/null || git add LICENSE NOTICE

    if git diff --cached --quiet; then
      echo "[license-rollout] SKIP unchanged: $repo_full"
      popd >/dev/null
      skip_count=$((skip_count + 1))
      continue
    fi

    git commit -m "$COMMIT_MESSAGE" >/dev/null 2>&1

    if [[ $PUSH_CHANGES -eq 1 ]]; then
      git push -u origin "$BRANCH_NAME" >/dev/null 2>&1
      echo "[license-rollout] PUSHED: $repo_full"

      if [[ $CREATE_PR -eq 1 ]]; then
        gh pr create \
          --repo "$repo_full" \
          --base "$target_base" \
          --head "$BRANCH_NAME" \
          --title "$PR_TITLE" \
          --body "$PR_BODY" >/dev/null
        echo "[license-rollout] PR created: $repo_full"
      fi
    fi

    popd >/dev/null
    success_count=$((success_count + 1))
  done

  echo "[license-rollout] DONE success=$success_count skip=$skip_count fail=$fail_count"

  if [[ $fail_count -ne 0 ]]; then
    exit 1
  fi
}

main "$@"