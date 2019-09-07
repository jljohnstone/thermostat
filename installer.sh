#!/bin/bash

# installer.sh
#
# This installer sets up the thermostat monitor and creates a systemd entry.

declare -r APP_DIRECTORY="/opt/thermostat_manager/"
declare -r LOG_DIRECTORY="/opt/thermostat_manager/var/log/"
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


create_env_local() {
    local_env="${APP_DIRECTORY}.env.local"
    cp ${APP_DIRECTORY}.env $local_env
    sed -i '/^#/d' $local_env
    new_comment="# This file should NOT be committed to a repository.\n# (See the .gitignore file.)"
    sed -i "1s;^;${new_comment}\n;" $local_env
}


# Install the program.
install() {
    check_user
    print_separator
    printf "INSTALL THERMOSTAT MONITOR\n\n"
    printf "Installing application to ${APP_DIRECTORY}\n\n"

    printf "  * Creating application directory...\n"
    mkdir -p ${APP_DIRECTORY}
    if [ $? -ne 0 ]; then
        printf "\nFailed to create application directory.\nExiting.\n\n"
        exit 1
    fi

    printf "  * Creating log directory...\n"
    mkdir -p ${LOG_DIRECTORY}
    if [ $? -ne 0 ]; then
        printf "\nFailed to create log directory.\nExiting.\n\n"
        exit 1
    fi

    printf "  * Installing application files...\n"
    cp -rT ./src ${APP_DIRECTORY}
    if [ $? -ne 0 ]; then
        printf "\nFailed to install application files.\nExiting.\n\n"
        exit 1
    else
        printf "  * Creating .env.local...\n"
        create_env_local
    fi

    printf "  * Installing systemd service...\n"
    cp ./etc/systemd/system/thermostat.service ${SYSTEMD_TARGET}
    if [ $? -ne 0 ]; then
        printf "\nFailed to install systemd service.\nExiting.\n\n"
        exit 1
    fi

    printf "  * Applying permissions...\n"
    chmod 644 ${SYSTEMD_TARGET}
    if [ $? -ne 0 ]; then
        printf "\nFailed to set systemd service permissions.\nExiting.\n\n"
        exit 1
    fi

    printf "\nInstallation successful.\n"

    print_separator
    printf "NEXT STEPS\n\n"
    printf "Edit the configuration settings in the \".env.local\" file:\n"
    printf "  ${APP_DIRECTORY}.env.local\n\n"
    printf "Enable the systemd service to run the thermostat monitor at startup:\n"
    printf "  $ sudo systemctl enable thermostat\n\n"
    printf "Issue the start and status commands to run and verify the service:\n"
    printf "  $ sudo systemctl start thermostat\n"
    printf "  $ systemctl status thermostat\n\n"
    exit 0
}


# Uninstall the program.
uninstall() {
    check_user
    print_separator
    printf "UNINSTALL THERMOSTAT MONITOR\n\n"

    printf "  * Stopping and disabling any running instance...\n"
    systemctl stop thermostat
    systemctl disable thermostat

    printf "  * Removing application directory...\n"
    rm -rf ${APP_DIRECTORY}
    if [ $? -ne 0 ]; then
        printf "\nFailed to remove the application directory.\nExiting.\n\n"
        exit 1
    fi

    printf "  * Removing systemd configuration...\n"
    rm ${SYSTEMD_TARGET}
    if [ $? -ne 0 ]; then
        printf "\nFailed to remove the systemd service configuration.\nExiting.\n\n"
        exit 1
    fi

    printf "\nRemoval completed.\n\n"
    exit 0
}


# Provide a separator for STDOUT.
print_separator() {
    printf "\n%60s\n" | tr " " "*"
}


# Run the main entry point.
main "$@"
