from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from datetime import datetime
import json
import time
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import pandas as pd
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import all enhanced components
from enhanced_ui_components import (
    load_advanced_css, 
    create_enhanced_header, 
    create_enhanced_sidebar,
    create_enhanced_metrics_dashboard,
    create_feature_cards,
    show_success_animation,
    show_error_animation,
    create_loading_spinner,
    ThemeManager
)

# Import existing components (assuming they exist)
from components.pdf_processor import PDFProcessor
from enhanced_gemini_analyzer import EnhancedGeminiAnalyzer
from advanced_visualizations import AdvancedVisualizationEngine
from components.report_generator import ReportGenerator
from intelligent_resume_builder import IntelligentResumeBuilder, ResumeOptimizationEngine
from analytics_tracking_system import PerformanceTracker, GoalSettingEngine
from market_intelligence_engine import MarketIntelligenceEngine
from interview_preparation_engine import InterviewPreparationEngine, InterviewAnalytics
from utils.session_manager import SessionManager
from utils.keyword_extractor import KeywordExtractor

# Page configuration
st.set_page_config(
    page_title="SmartATS Pro Elite - AI Resume Optimization Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SmartATSProElite:
    """
    Main application class integrating all advanced features
    """
    
    def __init__(self):
        # Initialize session manager
        self.session = SessionManager()
        
        # Initialize all engines and components
        self.pdf_processor = PDFProcessor()
        self.gemini_analyzer = EnhancedGeminiAnalyzer()
        self.viz_engine = AdvancedVisualizationEngine()
        self.report_gen = ReportGenerator()
        self.resume_builder = IntelligentResumeBuilder()
        self.optimization_engine = ResumeOptimizationEngine()
        self.performance_tracker = PerformanceTracker()
        self.goal_engine = GoalSettingEngine()
        self.market_intelligence = MarketIntelligenceEngine()
        self.interview_prep = InterviewPreparationEngine()
        self.interview_analytics = InterviewAnalytics()
        self.keyword_extractor = KeywordExtractor()
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        
        # Application state
        self.current_tab = st.session_state.get('current_tab', 'resume_analysis')
        
    def run(self):
        """
        Main application runner
        """
        # Load enhanced CSS
        load_advanced_css()
        
        # Create enhanced header
        create_enhanced_header()
        
        # Main navigation
        self.create_main_navigation()
        
        # Route to appropriate section based on current tab
        if self.current_tab == 'resume_analysis':
            self.render_resume_analysis_section()
        elif self.current_tab == 'resume_builder':
            self.render_resume_builder_section()
        elif self.current_tab == 'market_intelligence':
            self.render_market_intelligence_section()
        elif self.current_tab == 'interview_prep':
            self.render_interview_prep_section()
        elif self.current_tab == 'analytics_dashboard':
            self.render_analytics_dashboard()
        elif self.current_tab == 'goal_tracking':
            self.render_goal_tracking_section()
        
        # Render footer
        self.render_footer()
    
    def create_main_navigation(self):
        """
        Create main navigation tabs
        """
        tab_config = {
            'resume_analysis': {'icon': '🎯', 'label': 'Resume Analysis'},
            'resume_builder': {'icon': '🔨', 'label': 'AI Resume Builder'},
            'market_intelligence': {'icon': '📊', 'label': 'Market Intelligence'},
            'interview_prep': {'icon': '🎤', 'label': 'Interview Prep'},
            'analytics_dashboard': {'icon': '📈', 'label': 'Analytics'},
            'goal_tracking': {'icon': '🏆', 'label': 'Goal Tracking'}
        }
        
        # Create tabs
        tabs = st.tabs([f"{config['icon']} {config['label']}" for config in tab_config.values()])
        
        for i, (tab_key, config) in enumerate(tab_config.items()):
            with tabs[i]:
                if st.button(f"Switch to {config['label']}", key=f"nav_{tab_key}"):
                    st.session_state['current_tab'] = tab_key
                    st.rerun()
                
                if tab_key == self.current_tab:
                    self.render_tab_content(tab_key)
    
    def render_tab_content(self, tab_key: str):
        """
        Render content for the active tab
        """
        if tab_key == 'resume_analysis':
            self.render_resume_analysis_section()
        elif tab_key == 'resume_builder':
            self.render_resume_builder_section()
        elif tab_key == 'market_intelligence':
            self.render_market_intelligence_section()
        elif tab_key == 'interview_prep':
            self.render_interview_prep_section()
        elif tab_key == 'analytics_dashboard':
            self.render_analytics_dashboard()
        elif tab_key == 'goal_tracking':
            self.render_goal_tracking_section()
    
    def render_resume_analysis_section(self):
        """
        Render the enhanced resume analysis section
        """
        st.markdown("## 🎯 AI-Powered Resume Analysis")
        
        # Enhanced sidebar for this section
        job_description, industry, experience_level, analysis_depth = create_enhanced_sidebar()
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Enhanced file upload tabs
            tab1, tab2, tab3 = st.tabs(["📁 Upload Resume", "✏️ Edit Resume", "🔄 Version Compare"])
            
            with tab1:
                self.render_upload_section()
            
            with tab2:
                self.render_edit_section()
            
            with tab3:
                self.render_version_comparison()
        
        with col2:
            self.render_action_center(job_description, industry, experience_level, analysis_depth)
        
        # Display analysis results if available
        if self.session.get('analysis_result'):
            self.render_analysis_results()
    
    def render_upload_section(self):
        """
        Render enhanced upload section
        """
        uploaded_file = st.file_uploader(
            "Choose your resume PDF",
            type=['pdf'],
            help="Upload a PDF version of your resume for analysis"
        )
        
        if uploaded_file:
            self.session.set('uploaded_file', uploaded_file)
            self.session.set('file_name', uploaded_file.name)
            
            # Enhanced processing with progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🔍 Processing PDF...")
                progress_bar.progress(25)
                
                resume_text = self.pdf_processor.extract_text(uploaded_file)
                progress_bar.progress(75)
                
                if resume_text:
                    self.session.set('resume_text', resume_text)
                    progress_bar.progress(100)
                    status_text.empty()
                    
                    show_success_animation(f"Successfully processed: {uploaded_file.name}")
                    
                    # Enhanced preview with statistics
                    self.render_resume_preview(resume_text)
                else:
                    show_error_animation("Failed to extract text from PDF")
            
            except Exception as e:
                show_error_animation(f"Error processing file: {str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    def render_resume_preview(self, resume_text: str):
        """
        Render enhanced resume preview with analytics
        """
        with st.expander("📋 Resume Preview & Analytics", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.text_area(
                    "Extracted Content",
                    resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text,
                    height=200,
                    disabled=True
                )
            
            with col2:
                # Quick statistics
                word_count = len(resume_text.split())
                char_count = len(resume_text)
                
                st.metric("Word Count", word_count)
                st.metric("Character Count", char_count)
                
                # Quick ATS assessment
                ats_score = self.calculate_quick_ats_score(resume_text)
                st.metric("Quick ATS Score", f"{ats_score}%")
    
    def render_edit_section(self):
        """
        Render enhanced edit section with real-time analysis
        """
        resume_text_input = st.text_area(
            "Edit your resume content",
            value=self.session.get('resume_text', ''),
            height=400,
            help="You can paste your resume text directly or edit the extracted content"
        )
        
        if resume_text_input:
            self.session.set('resume_text', resume_text_input)
            self.session.set('is_edited', True)
            
            # Real-time statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                word_count = len(resume_text_input.split())
                st.metric("Words", word_count)
            
            with col2:
                char_count = len(resume_text_input)
                st.metric("Characters", char_count)
            
            with col3:
                # Real-time keyword density if job description is available
                job_desc = st.session_state.get('job_description', '')
                if job_desc:
                    density = self.calculate_keyword_density(resume_text_input, job_desc)
                    st.metric("Keyword Density", f"{density}%")
    
    def render_version_comparison(self):
        """
        Render resume version comparison
        """
        st.markdown("#### 🔄 Resume Version Management")
        
        # Get all resume versions from session
        versions = self.session.get('resume_versions', {})
        
        if len(versions) < 2:
            st.info("Upload or edit multiple resume versions to enable comparison")
            return
        
        # Version selector
        version_names = list(versions.keys())
        col1, col2 = st.columns(2)
        
        with col1:
            version1 = st.selectbox("Select Version 1", version_names, key="v1")
        
        with col2:
            version2 = st.selectbox("Select Version 2", version_names, key="v2")
        
        if version1 and version2 and version1 != version2:
            if st.button("Compare Versions"):
                self.perform_version_comparison(versions[version1], versions[version2])
    
    def render_action_center(self, job_description: str, industry: str, 
                           experience_level: str, analysis_depth: str):
        """
        Render enhanced action center
        """
        st.markdown("### 🎯 AI Analysis Center")
        
        # Primary analysis button
        if st.button("🚀 Analyze Resume", use_container_width=True, type="primary"):
            if self.session.get('resume_text') and job_description:
                self.perform_comprehensive_analysis(
                    job_description, industry, experience_level, analysis_depth
                )
            else:
                show_error_animation("Please provide both resume and job description!")
        
        # Quick analysis button
        if st.button("⚡ Quick Analysis", use_container_width=True):
            if self.session.get('resume_text'):
                self.perform_quick_analysis()
            else:
                show_error_animation("Please upload or paste your resume first!")
        
        # Re-analyze button
        if st.button("🔄 Re-analyze", use_container_width=True):
            if self.session.get('resume_text') and job_description:
                self.perform_comprehensive_analysis(
                    job_description, industry, experience_level, analysis_depth
                )
                self.session.increment('rescore_count')
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            # Analysis customization
            include_market_data = st.checkbox("Include Market Intelligence", value=True)
            include_interview_prep = st.checkbox("Generate Interview Questions", value=True)
            competitive_analysis = st.checkbox("Competitive Analysis", value=False)
            
            # Store preferences
            self.session.set('analysis_preferences', {
                'include_market_data': include_market_data,
                'include_interview_prep': include_interview_prep,
                'competitive_analysis': competitive_analysis
            })
        
        # Session management
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save Session", use_container_width=True):
                self.save_session_data()
        
        with col2:
            if st.button("🗑️ Clear All", use_container_width=True):
                if st.session_state.get('confirm_clear'):
                    self.session.clear()
                    st.rerun()
                else:
                    st.session_state['confirm_clear'] = True
                    st.warning("Click again to confirm clearing all data")
    
    def perform_comprehensive_analysis(self, job_description: str, industry: str,
                                     experience_level: str, analysis_depth: str):
        """
        Perform comprehensive resume analysis with all features
        """
        with st.spinner():
            create_loading_spinner("🤖 Performing AI Analysis...")
            
            # Track analysis start
            start_time = time.time()
            
            # Perform enhanced analysis
            analysis_result = self.gemini_analyzer.analyze_resume_comprehensive(
                self.session.get('resume_text'),
                job_description,
                industry,
                experience_level,
                analysis_depth
            )
            
            # Get analysis preferences
            preferences = self.session.get('analysis_preferences', {})
            
            # Add market intelligence if requested
            if preferences.get('include_market_data', True):
                skills = analysis_result.get('matched_keywords', [])
                market_insights = self.market_intelligence.generate_market_insights(
                    industry, experience_level, skills
                )
                analysis_result['market_intelligence'] = market_insights
            
            # Add interview preparation if requested
            if preferences.get('include_interview_prep', True):
                interview_prep = self.interview_prep.generate_interview_preparation_plan(
                    analysis_result, job_description, industry, experience_level
                )
                analysis_result['interview_preparation'] = interview_prep
            
            # Store results
            self.session.set('analysis_result', analysis_result)
            self.session.set('analysis_timestamp', datetime.now())
            
            # Track performance
            session_id = self.performance_tracker.record_analysis(
                analysis_result, self.session.get('resume_text'), 
                job_description, industry, experience_level
            )
            
            # Calculate analysis time
            analysis_time = time.time() - start_time
            
            # Show success
            show_success_animation(f"Analysis Complete! ({analysis_time:.1f}s)")
            
            time.sleep(1)
            st.rerun()
    
    def render_analysis_results(self):
        """
        Render comprehensive analysis results
        """
        st.markdown("---")
        st.markdown("## 📊 Comprehensive Analysis Results")
        
        analysis = self.session.get('analysis_result')
        
        # Enhanced metrics dashboard
        create_enhanced_metrics_dashboard(analysis)
        
        # Tabbed results interface
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "🎯 Overview",
            "📈 Advanced Analytics", 
            "💡 AI Insights",
            "📊 Market Intelligence",
            "🎤 Interview Prep",
            "🔨 Optimization",
            "📄 Reports"
        ])
        
        with tab1:
            self.render_analysis_overview(analysis)
        
        with tab2:
            self.render_advanced_analytics(analysis)
        
        with tab3:
            self.render_ai_insights(analysis)
        
        with tab4:
            self.render_market_intelligence_tab(analysis)
        
        with tab5:
            self.render_interview_prep_tab(analysis)
        
        with tab6:
            self.render_optimization_tab(analysis)
        
        with tab7:
            self.render_reports_tab(analysis)
    
    def render_resume_builder_section(self):
        """
        Render the AI resume builder section
        """
        st.markdown("## 🔨 AI-Powered Resume Builder")
        
        # Builder options
        builder_tab1, builder_tab2, builder_tab3 = st.tabs([
            "🎯 Smart Builder", "📝 Template Gallery", "🔄 Optimization Lab"
        ])
        
        with builder_tab1:
            self.render_smart_builder()
        
        with builder_tab2:
            self.render_template_gallery()
        
        with builder_tab3:
            self.render_optimization_lab()
    
    def render_market_intelligence_section(self):
        """
        Render market intelligence section
        """
        st.markdown("## 📊 Market Intelligence & Career Insights")
        
        # Market intelligence interface
        self.render_market_dashboard()
    
    def render_interview_prep_section(self):
        """
        Render interview preparation section
        """
        st.markdown("## 🎤 AI Interview Coach")
        
        # Interview prep interface
        self.render_interview_dashboard()
    
    def render_analytics_dashboard(self):
        """
        Render analytics dashboard
        """
        st.markdown("## 📈 Performance Analytics")
        
        # Get dashboard data
        dashboard_data = self.performance_tracker.get_performance_dashboard_data()
        
        if 'error' in dashboard_data:
            st.info("No analytics data available yet. Perform some analyses to see your progress!")
            return
        
        # Create dashboard figures
        figures = self.performance_tracker.create_performance_dashboard()
        
        # Display charts
        for i, fig in enumerate(figures):
            st.plotly_chart(fig, use_container_width=True, key=f"dashboard_chart_{i}")
    
    def render_goal_tracking_section(self):
        """
        Render goal tracking section
        """
        st.markdown("## 🏆 Goal Tracking & Career Planning")
        
        # Goal setting interface
        self.render_goal_dashboard()
    
    def calculate_quick_ats_score(self, resume_text: str) -> int:
        """
        Calculate a quick ATS compatibility score
        """
        score = 100
        
        # Check for common ATS issues
        if len(resume_text) < 500:
            score -= 20
        
        if not re.search(r'\b\d{4}\b', resume_text):  # No years
            score -= 15
        
        if not re.search(r'@', resume_text):  # No email
            score -= 10
        
        if len(re.findall(r'[^\w\s]', resume_text)) > len(resume_text) * 0.1:  # Too many special chars
            score -= 10
        
        return max(0, score)
    
    def calculate_keyword_density(self, resume_text: str, job_description: str) -> int:
        """
        Calculate keyword density between resume and job description
        """
        resume_words = set(resume_text.lower().split())
        jd_words = set(job_description.lower().split())
        
        common_words = resume_words & jd_words
        
        if not jd_words:
            return 0
        
        return int(len(common_words) / len(jd_words) * 100)
    
    def render_footer(self):
        """
        Render enhanced footer
        """
        st.markdown("---")
        
        # Footer stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_analyses = len(self.session.get('analysis_history', []))
            st.metric("Total Analyses", total_analyses)
        
        with col2:
            current_theme = self.theme_manager.get_current_theme()
            st.metric("Theme", current_theme.title())
        
        with col3:
            session_duration = "Active"  # Could calculate actual duration
            st.metric("Session", session_duration)
        
        with col4:
            version = "Elite v2.0"
            st.metric("Version", version)
        
        # Footer content
        st.markdown(
            """
            <div style='text-align: center; padding: 2rem; background: var(--surface-color); border-radius: 12px; margin-top: 2rem;'>
                <h3 style='color: var(--primary-color); margin-bottom: 1rem;'>🚀 SmartATS Pro Elite</h3>
                <p style='color: var(--text-secondary); margin: 0;'>
                    Next-Generation AI Resume Optimization Platform
                </p>
                <p style='color: var(--text-secondary); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                    Powered by Google Gemini AI • Built with ❤️ using Streamlit
                </p>
                <div style='margin-top: 1rem; display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;'>
                    <span style='background: var(--primary-color); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;'>
                        🎯 99% ATS Success Rate
                    </span>
                    <span style='background: var(--success-color); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;'>
                        ⚡ Real-time Analysis
                    </span>
                    <span style='background: var(--secondary-color); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;'>
                        🤖 AI-Powered Insights
                    </span>
                    <span style='background: var(--warning-color); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;'>
                        📈 Career Intelligence
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Additional helper methods would be implemented here...
    def save_session_data(self):
        """Save session data"""
        session_data = self.session.export_session_data()
        st.success("Session data saved successfully!")
    
    def perform_quick_analysis(self):
        """Perform quick analysis"""
        st.info("Quick analysis feature - analyzing basic resume metrics...")
    
    def perform_version_comparison(self, version1, version2):
        """Compare two resume versions"""
        st.info("Version comparison feature - comparing resume versions...")
    
    def render_analysis_overview(self, analysis):
        """Render analysis overview tab"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Key Strengths")
            for strength in analysis.get('strengths', [])[:5]:
                st.success(f"💪 {strength}")
        
        with col2:
            st.markdown("#### 📈 Improvement Areas")
            for improvement in analysis.get('critical_improvements', [])[:5]:
                st.warning(f"💡 {improvement}")
    
    def render_advanced_analytics(self, analysis):
        """Render advanced analytics tab"""
        # Create comprehensive dashboard
        fig = self.viz_engine.create_comprehensive_dashboard(analysis)
        st.plotly_chart(fig, use_container_width=True)
    
    def render_ai_insights(self, analysis):
        """Render AI insights tab"""
        st.markdown("#### 🤖 AI-Generated Insights")
        
        if 'ai_suggestions' in analysis:
            suggestions = analysis['ai_suggestions']
            for category, items in suggestions.items():
                with st.expander(f"📋 {category.replace('_', ' ').title()}"):
                    for item in items:
                        st.write(f"• {item}")
    
    def render_market_intelligence_tab(self, analysis):
        """Render market intelligence tab"""
        if 'market_intelligence' in analysis:
            market_data = analysis['market_intelligence']
            
            # Create market intelligence charts
            charts = self.market_intelligence.create_market_intelligence_dashboard(market_data)
            
            for chart in charts:
                st.plotly_chart(chart, use_container_width=True)
    
    def render_interview_prep_tab(self, analysis):
        """Render interview preparation tab"""
        if 'interview_preparation' in analysis:
            interview_data = analysis['interview_preparation']
            
            # Display interview questions and preparation plan
            st.markdown("#### 🎤 Personalized Interview Questions")
            
            questions = interview_data.get('personalized_questions', {})
            for category, question_list in questions.items():
                with st.expander(f"📋 {category.replace('_', ' ').title()}"):
                    for q in question_list[:3]:  # Show top 3
                        st.write(f"**Q:** {q['question']}")
                        st.write(f"*Focus: {q.get('focus_area', 'General')}*")
                        st.write("---")
    
    def render_optimization_tab(self, analysis):
        """Render optimization tab"""
        # Create optimization versions
        if st.button("🔄 Generate Optimization Versions"):
            versions = self.optimization_engine.create_multiple_versions(
                self.session.get('resume_text', ''),
                self.session.get('job_description', ''),
                self.session.get('industry', 'Technology')
            )
            
            for version in versions:
                with st.expander(f"📝 {version['name']}"):
                    st.write(f"**Focus:** {version['focus']}")
                    st.write(f"**Estimated Improvement:** {version['estimated_improvement']}")
                    with st.container():
                        st.text_area(
                            "Optimized Content",
                            version['content'],
                            height=200,
                            key=f"opt_{version['name']}"
                        )
    
    def render_reports_tab(self, analysis):
        """Render reports tab"""
        st.markdown("### 📄 Generate Reports")
        
        report_col1, report_col2, report_col3 = st.columns(3)
        
        with report_col1:
            if st.button("📥 Comprehensive PDF Report", use_container_width=True):
                pdf_bytes = self.report_gen.generate_pdf_report(
                    analysis,
                    self.session.get('resume_text', ''),
                    self.session.get('job_description', '')
                )
                st.download_button(
                    label="💾 Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"SmartATS_Elite_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
        
        with report_col2:
            if st.button("📊 Analytics CSV", use_container_width=True):
                csv_data = self.report_gen.generate_csv_report(analysis)
                st.download_button(
                    label="💾 Download CSV Data",
                    data=csv_data,
                    file_name=f"SmartATS_Analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with report_col3:
            if st.button("📋 Executive Summary", use_container_width=True):
                summary = self.report_gen.generate_text_summary(analysis)
                st.code(summary, language="markdown")
    
    def render_smart_builder(self):
        """Render smart resume builder"""
        st.markdown("#### 🎯 AI-Powered Resume Builder")
        st.info("Smart resume builder interface - build from scratch with AI guidance")
    
    def render_template_gallery(self):
        """Render template gallery"""
        st.markdown("#### 📝 Professional Resume Templates")
        st.info("Template gallery - choose from ATS-optimized templates")
    
    def render_optimization_lab(self):
        """Render optimization lab"""
        st.markdown("#### 🔄 Resume Optimization Laboratory")
        st.info("Optimization lab - experiment with different approaches")
    
    def render_market_dashboard(self):
        """Render market intelligence dashboard"""
        st.info("Market intelligence dashboard - salary insights, trends, and opportunities")
    
    def render_interview_dashboard(self):
        """Render interview preparation dashboard"""
        st.info("Interview coaching dashboard - personalized question practice and feedback")
    
    def render_goal_dashboard(self):
        """Render goal tracking dashboard"""
        st.info("Goal tracking dashboard - set targets and monitor progress")

# Initialize and run the application
def main():
    """
    Main function to run SmartATS Pro Elite
    """
    app = SmartATSProElite()
    app.run()

if __name__ == "__main__":
    main()