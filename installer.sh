#!/bin/bash

# installer.sh
#
# This installer sets up the thermostat monitor and creates a systemd entry.

declare -r APP_DIRECTORY="/opt/thermostat_manager/"
declare -r SYSTEMD_TARGET="/etc/systemd/system/thermostat.service"


# The main entry point with options.
main() {

    if [[ ! $@ =~ ^\-.+ ]]; then
        install
        exit 0
    fi

    # Get command arguments
    OPTIND=1
    while getopts hiu opt; do

        case $opt in
            h)
                print_help
                exit 0
                ;;
            i)
                install
                ;;
            u)
                uninstall
                ;;
            \?)
                printf "\nOption not recognized. Use -h for help.\n"
                exit 1
                ;;
        esac
    done

    shift "$((OPTIND-1))"
}


check_user() {
    if [[ $EUID -ne 0 ]]; then
        printf "\nSetup must be run with root privileges. Exiting the program.\n\n"
        exit 1
    fi
}


print_help() {
    help=$(cat <<EOF
Manage a thermostat monitor installation.
Usage: installer.sh [ARGUMENT]...
Arguments:
    -i,        install the monitor
    -u,        uninstall the monitor
    -h,        display this help
EOF
)
    echo "$help"
}


# Install the program.
install() {
    check_user
    print_separator
    printf "Installing\n"

}


# Uninstall the program.
uninstall() {
    check_user
    print_separator
    printf "Uninstalling\n"

}


# Provide a separator for STDOUT.
print_separator() {
    printf "\n%60s\n" | tr " " "*"
}


# Run the main entry point.
main "$@"
