# Process Governance, Change Control, and Safety

## Immutable Safety Rules
1. **No Autonomous Policy Deletion**: AI agents cannot delete or relax mandatory compliance gates.
2. **Four-Eyes Approval**: High-impact production workflow adjustments require multi-stakeholder authorization.
3. **Segregation of Duties (SoD)**: Automatic detection and blocking of toxic role combinations (e.g., PO Creator cannot approve PO).
4. **Mandatory Rollback Plans**: No change request is approved without an automated rollback procedure and baseline benchmark snapshot.
5. **Continuous Drift Monitoring**: Real-time alerting if observed behavior deviates > 5% from approved baseline.\n