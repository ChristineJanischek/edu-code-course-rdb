#!/usr/bin/env bash

# Shared helpers for the custom Christine Janischek license policy.
# This file is sourced by operational scripts.

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

apply_custom_license_policy() {
  local repo_root="$1"
  write_license_files "$repo_root"
  ensure_readme_notice "$repo_root"
}