# Bottleneck Detection and Heatmap Intelligence

## Constraint Detection
Bottlenecks are identified through multi-variate statistical profiling:
- **Queue Length**: Number of pending cases awaiting execution.
- **Wait Time vs. Service Time**: Ratio of idle queue latency to active processing.
- **Resource Saturation**: Utilization percentage of allocated actors or systems.
- **Throughput Drop**: Degradation in completions per unit time.

## Visual Heatmap
Activities and handoffs are color-coded:
- Green: Flow velocity > 95% of SLA benchmark.
- Amber: Wait time exceeding 1.5x standard deviation.
- Red: Critical constraint causing upstream queuing and SLA breach risk.\n