# 🚀 **AGENT QUICK START GUIDE**
## **Repository Cleanup for Dadudekc Portfolio**

---

## 📋 **IMMEDIATE START INSTRUCTIONS**

### **1. Download Required Files**
- `repository_cleanup_script.ps1` - Single repository cleanup
- `batch_cleanup_script.ps1` - Batch processing for multiple repositories
- `REPOSITORY_CLEANUP_STRATEGY.md` - Complete strategy document

### **2. Verify Prerequisites**
```powershell
# Check if Git is installed
git --version

# Check if GitHub CLI is installed (optional but recommended)
gh --version

# Check PowerShell execution policy
Get-ExecutionPolicy
```

### **3. Set Execution Policy (if needed)**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎯 **QUICK START COMMANDS**

### **For Single Repository Cleanup**
```powershell
# Navigate to your workspace
cd "D:\repos\Dadudekc"

# Clean up a single repository
.\repository_cleanup_script.ps1 "Agent-5"

# Clean up another repository
.\repository_cleanup_script.ps1 "ai-task-organizer"
```

### **For Batch Repository Cleanup**
```powershell
# Clean up Agent-1 repositories (high priority)
.\batch_cleanup_script.ps1 -AgentNumber "1"

# Clean up Agent-2 repositories (medium priority)
.\batch_cleanup_script.ps1 -AgentNumber "2"

# Clean up custom repository list
.\batch_cleanup_script.ps1 -RepositoryList "Agent-5,ai-task-organizer,network-scanner"
```

---

## 📅 **DAILY WORKFLOW**

### **Morning (9:00 AM)**
1. **Check Daily Assignment**: Review which repositories you're responsible for
2. **Run Batch Cleanup**: Use batch script for efficiency
3. **Review Results**: Check for any errors or issues

### **Afternoon (2:00 PM)**
1. **Manual Review**: Handle any repositories with errors
2. **PR Management**: Review and merge valuable pull requests
3. **Documentation**: Update cleanup reports

### **Evening (6:00 PM)**
1. **Submit Daily Report**: Use the template below
2. **Plan Next Day**: Identify any remaining work
3. **Coordinate**: Communicate with other agents if needed

---

## 📊 **DAILY REPORT TEMPLATE**

```
=== AGENT-[X] DAILY REPORT ===
Date: [TODAY'S DATE]
Agent: [YOUR NAME]
Repositories Cleaned: [X]/[TARGET]
Branches Removed: [COUNT]
PRs Merged: [COUNT]
Issues Encountered: [DESCRIPTION]
Next Day Plan: [PLAN]
Status: [ON_TRACK/BEHIND/AHEAD]

=== REPOSITORIES PROCESSED ===
[REPO_NAME]: [STATUS] - [BRANCHES_REMOVED] branches removed
[REPO_NAME]: [STATUS] - [BRANCHES_REMOVED] branches removed

=== ISSUES & SOLUTIONS ===
[ISSUE]: [SOLUTION_APPLIED]

=== NEXT DAY PRIORITIES ===
1. [PRIORITY_1]
2. [PRIORITY_2]
3. [PRIORITY_3]
```

---

## 🔧 **COMMON ISSUES & SOLUTIONS**

### **Issue: "Git is not available"**
**Solution**: Install Git from https://git-scm.com/

### **Issue: "Execution policy error"**
**Solution**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### **Issue: "Repository not found"**
**Solution**: Verify the repository exists in `D:\repos\Dadudekc\`

### **Issue: "Permission denied"**
**Solution**: Check if you have write access to the repository

### **Issue: "Uncommitted changes"**
**Solution**: Commit or stash changes before cleanup
```powershell
git add .
git commit -m "Save work before cleanup"
# OR
git stash push -m "Stash before cleanup"
```

---

## 📈 **PROGRESS TRACKING**

### **Daily Targets**
- **Agent-1**: 6 repositories per day (Days 1-3)
- **Agent-2**: 6 repositories per day (Days 4-6)
- **Agent-3**: 6 repositories per day (Days 7-9)
- **Agent-4**: 5+ repositories per day (Days 10-12)

### **Success Metrics**
- **Quantitative**: Repositories cleaned, branches removed, PRs merged
- **Qualitative**: 100% standardization, zero stale branches

---

## 🚨 **EMERGENCY PROCEDURES**

### **If Script Fails**
1. **Stop immediately** - Don't continue with broken script
2. **Document the error** - Copy error message exactly
3. **Manual cleanup** - Use git commands directly
4. **Report issue** - Contact coordinator immediately

### **If Repository Becomes Unusable**
1. **Don't panic** - Git operations are reversible
2. **Check git status** - See what happened
3. **Use git reflog** - Find previous state
4. **Reset if needed** - `git reset --hard HEAD~1`

---

## 💡 **PRO TIPS**

### **Efficiency Tips**
1. **Use batch script** for multiple repositories
2. **Run during off-peak hours** to avoid conflicts
3. **Keep PowerShell window open** to avoid repeated setup
4. **Use tab completion** for repository names

### **Quality Tips**
1. **Always verify cleanup** - Check final branch count
2. **Document everything** - Create detailed reports
3. **Test on one repo first** - Before running batch
4. **Backup important work** - Before major cleanup

---

## 📞 **SUPPORT & COORDINATION**

### **When to Contact Coordinator**
- Script errors that prevent work
- Repository access issues
- Unusual git situations
- Progress falling behind schedule

### **Communication Channels**
- Daily reports (required)
- Immediate issues (urgent)
- General questions (as needed)

---

## 🎯 **SUCCESS CHECKLIST**

### **Before Starting Each Day**
- [ ] Scripts downloaded and tested
- [ ] Git credentials verified
- [ ] Daily assignment reviewed
- [ ] Previous day's issues resolved

### **During Work**
- [ ] Follow cleanup procedures exactly
- [ ] Document all actions taken
- [ ] Handle errors immediately
- [ ] Maintain progress pace

### **End of Day**
- [ ] All assigned repositories processed
- [ ] Daily report submitted
- [ ] Next day planned
- [ ] Issues documented and reported

---

## 🚀 **READY TO START?**

### **Quick Test**
```powershell
# Test with a single repository first
.\repository_cleanup_script.ps1 "Agent-5"
```

### **If Test Succeeds**
```powershell
# Run your daily batch
.\batch_cleanup_script.ps1 -AgentNumber "[YOUR_AGENT_NUMBER]"
```

### **Remember**
- **Follow the process exactly**
- **Document everything**
- **Report issues immediately**
- **Stay on schedule**

---

*This guide gets you started immediately. For complete details, refer to `REPOSITORY_CLEANUP_STRATEGY.md`*

**Good luck with the cleanup! Your work is critical for the portfolio transformation! 🎯✨**
