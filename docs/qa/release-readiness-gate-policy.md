# Release Readiness Gate & Quality Score Policy

## 1. Quality Score Formula

The Release Readiness Score (0-100) is calculated deterministically:

$$\text{Readiness Score} = (\text{Test Pass Ratio} \times 70) + (\text{UAT Approval} \times 20) + (\text{High Defect Penalty})$$

Where:
- **Test Pass Ratio**: Passed test count / Total test count (Max 70 pts).
- **UAT Approval**: 20 pts if client formal UAT sign-off granted; 0 pts otherwise.
- **High Defect Penalty**: 10 pts if 0 high defects; minus 5 pts per open high defect.

---

## 2. Deterministic Quality Gate Blocking Rules

Regardless of readiness score, a release candidate is **STRICTLY BLOCKED** if ANY of the following conditions exist:

1. **Failing Test Cases**: $>\!0$ failing tests in the active execution run.
2. **Open Critical Defects**: $>\!0$ unresolved `CRITICAL` severity defects.
3. **Missing UAT Sign-off**: Client UAT sign-off has not been formally granted.

AI scores cannot override these hard blocking rules.
