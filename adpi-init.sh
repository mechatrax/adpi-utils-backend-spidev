#!/bin/bash

set -e

CONF_FILE=/etc/adpi.conf
LIB_PATH=/usr/lib/adpi-utils/

[ -r $CONF_FILE ]

SECTIONS=$(${LIB_PATH}/parse_sections.sh $CONF_FILE)

export_params ()
{
  local p
  local params

  SPI_NAME=$1
  params=$(${LIB_PATH}/parse_parameters.sh $1 $CONF_FILE)
  for p in $params
  do
    case $p in
    device*)
      DEVICE_NAME=$(echo $p | cut -d= -f2)
      ;;
    eeprom*)
      EEPROM_NAME=1-00$(echo $p | cut -d= -f2 | sed -e 's/^0x//')
      ;;
    gpio*)
      GPIO_NAME=1-00$(echo $p | cut -d= -f2 | sed -e 's/^0x//')
      ;;
    *)
      ;;
    esac
  done
}

execute_backend ()
{
  ${LIB_PATH}/adpi-utils-backend \
    device=$DEVICE_NAME spi=$SPI_NAME eeprom=$EEPROM_NAME gpio=$GPIO_NAME $@
}

for s in $SECTIONS
do
  DEVICE_NAME=""
  export_params $s
  if [ "$DEVICE_NAME" != "" ]
  then
    execute_backend reset
    execute_backend set gain 1
    execute_backend set frequency 470
  fi
done

