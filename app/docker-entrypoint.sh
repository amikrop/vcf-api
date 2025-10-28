#!/bin/sh
set -e

USER="webuser"
GROUP="webgroup"

fix_perms_if_needed() {
    path="$1"
    [ -e "$path" ] || return 0
    current_uid=$(stat -c "%u" "$path" 2>/dev/null || true)
    target_uid=$(id -u "$USER")
    [ -n "$current_uid" ] && [ "$current_uid" -ne "$target_uid" ] && \
        chown -R "$USER:$GROUP" "$path" 2>/dev/null || true
}

fix_perms_if_needed "/home/webuser/data"
fix_perms_if_needed "/home/webuser/app/vcf/tests/variants.vcf.test"

exec su-exec "$USER" "$@"
