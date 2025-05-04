FROM justb4/jmeter:latest

USER root

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Create directories for JMeter test plan and results
RUN mkdir -p /opt/jmeter && \
    mkdir -p /opt/jmeter/results
# Copy the JMeter test plan to the container
COPY plan.jmx /opt/jmeter/plan.jmx
COPY run_test.sh /usr/local/bin/run_test.sh
RUN chmod +x /usr/local/bin/run_test.sh

VOLUME ["/opt/jmeter/results"]

# Create a cronjob to run the JMeter test every hour
RUN echo "0 * * * * root /usr/local/bin/run_test.sh >> /var/log/cron.log 2>&1" \
    > /etc/cron.d/jmeter_cron \
    && chmod 0644 /etc/cron.d/jmeter_cron \
    && crontab /etc/cron.d/jmeter_cron

# Execute cron in the foreground
CMD ["cron", "-f"]