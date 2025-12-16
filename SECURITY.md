# Security Notice

## API Key Security

### Important: API Key Rotation Required

**⚠️ SECURITY ALERT**: A Groq API key was previously exposed in the git history of this repository. 

**Action Required:**
1. **Rotate your API key immediately** if you were using the exposed key
2. Revoke the old API key from [Groq Console](https://console.groq.com/)
3. Generate a new API key and update your `.env` file

### Current Security Status

✅ **Code Configuration**: All code now correctly loads the API key from the `.env` file only
✅ **Git Configuration**: The `.env` file is properly excluded from version control via `.gitignore`
✅ **No Hardcoded Keys**: No API keys are hardcoded in the source code

### Best Practices

1. **Never commit API keys** to version control
2. **Always use environment variables** for sensitive credentials
3. **Rotate keys immediately** if exposed
4. **Use `.env.example`** as a template (without real keys)
5. **Keep `.env` in `.gitignore`** (already configured)

### Git History

The exposed API key exists in commit history. For private repositories or early-stage projects, you may consider:
- Using `git filter-repo` to remove sensitive data from history (requires force push)
- Creating a new repository if the exposure is critical

For production repositories, the recommended approach is to rotate the key rather than rewriting history.

### Reporting Security Issues

If you discover any security vulnerabilities, please report them responsibly.

