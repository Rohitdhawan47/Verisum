# Changelog

All notable changes to VeriSum will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### In Progress
- GROBID parser integration for improved academic document structure extraction
- UI/UX refinements and polish
- Enhanced error handling and user feedback

### Planned
- OCR support for scanned PDFs
- Multi-language summarization
- Export functionality (Word, PDF, Markdown)
- Batch processing API
- User authentication system

---

## [0.1.0] - 2025-02 (Current)

### ✨ Features
- **PDF Summarization**: Core AI-powered summarization using LED model
- **Smart Parsing**: Advanced PyMuPDF-based parser with layout detection
- **GPU Acceleration**: Kaggle P100 GPU backend for fast processing
- **Streamlit UI**: Interactive web interface with real-time processing
- **Keyword Extraction**: Automatic anchor word generation using KeyBERT
- **Color-Coded Display**: Visual highlighting to match summaries with source text
- **Flexible Page Selection**: Process specific pages, ranges, or entire documents
- **ngrok Integration**: Secure tunneling between local frontend and Kaggle backend

### 🏗️ Architecture
- FastAPI backend on Kaggle
- Streamlit frontend (local)
- ngrok tunnel for connectivity
- LED (Longformer Encoder-Decoder) model fine-tuned on arXiv
- KeyBERT for keyword extraction
- PyMuPDF for PDF parsing

### 📝 Documentation
- Comprehensive README with setup instructions
- ngrok configuration guide
- Troubleshooting section
- Dependencies documentation

### ⚠️ Known Issues
- UI is functional but needs visual polish
- Table content is filtered out, not summarized
- Limited to English language
- No authentication/multi-user support
- Occasional chunking fragmentation with very long paragraphs

### 🎯 Project Status
- **State**: Functional Beta
- **Development**: Solo project, active development
- **Stability**: Core features work reliably
- **Production Readiness**: Not recommended for production use yet

---

## Development Notes

### Parser Evolution
1. **v0.1.0 (Current)**: PyMuPDF-based parser
   - Strengths: Fast, reliable, handles most PDFs well
   - Limitations: Struggles with complex layouts, citations, and tables
   
2. **v0.2.0 (Planned)**: GROBID parser integration
   - Goal: Better academic document structure extraction
   - Status: Experimental development
   - Expected: Improved citation handling, section recognition

### Performance Targets
- Current: ~2-3 pages/minute with GPU
- Target: ~5-10 pages/minute with optimizations

### Technical Debt
- Refactor chunking logic for better paragraph detection
- Improve error messages and user feedback
- Add comprehensive unit tests
- Implement logging system
- Create proper configuration management

---

## Version History Summary

| Version | Status | Release Date | Key Features |
|---------|--------|--------------|--------------|
| 0.1.0 | Current | Feb 2025 | Core summarization, PyMuPDF parser, Streamlit UI |
| 0.2.0 | Planned | TBD | GROBID parser, UI polish, better error handling |
| 1.0.0 | Future | TBD | Production-ready, auth, multi-language, OCR |

---

## Contributing to Changelog

When contributing, please update this file following these guidelines:

### Format
```markdown
### Added
- New features

### Changed  
- Changes to existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements
```

### Example Entry
```markdown
## [0.2.0] - 2025-04-15

### Added
- GROBID parser as alternative to PyMuPDF
- Export summaries to Word document
- Dark mode toggle

### Fixed
- Chunking fragmentation for long paragraphs
- ngrok connection timeout handling
```

---

## Roadmap Milestones

### v0.2.0 - "Parser Upgrade" (Target: Q2 2025)
- [ ] GROBID parser integration
- [ ] UI visual improvements
- [ ] Better error messages
- [ ] Configuration file support

### v0.3.0 - "Export & Polish" (Target: Q3 2025)
- [ ] Export to Word/PDF/Markdown
- [ ] Save session history
- [ ] Improved color scheme
- [ ] Mobile-responsive design

### v0.4.0 - "Intelligence" (Target: Q4 2025)
- [ ] Multi-language support
- [ ] Custom model fine-tuning UI
- [ ] Summary quality metrics
- [ ] A/B testing different summarization strategies

### v1.0.0 - "Production Ready" (Target: 2026)
- [ ] User authentication
- [ ] Database integration
- [ ] API rate limiting
- [ ] Comprehensive testing suite
- [ ] Production deployment guide
- [ ] Monitoring and analytics

---

## Feedback & Suggestions

Have ideas for VeriSum? Here's how to share them:

1. **Feature Requests**: Open a GitHub Issue with the "enhancement" label
2. **Bug Reports**: Open a GitHub Issue with the "bug" label
3. **General Discussion**: Use GitHub Discussions
4. **Direct Contact**: Comment on the Kaggle notebook

---

**Note**: As a solo-developed project, timelines are estimates and may shift based on complexity, available time, and community priorities.

**Last Updated**: February 2025
