#!/usr/bin/env bash

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RESULT_DIR=/opt/jmeter/results

# Execute JMeter in non-GUI mode
jmeter -n \
  -t /opt/jmeter/plan.jmx \
  -l "$RESULT_DIR/resultados_$TIMESTAMP.jtl" \
  -e -o "$RESULT_DIR/html_report_$TIMESTAMP"

echo "[JMeter] Test completat a $TIMESTAMP"