import React from 'react';
import './styles/Footer.css';


function Footer() {
    return (
        <footer>
            <div className="copyright">&#169; 2023</div>
            <div className="disclaimer">This project is not in any way affiliated or endorsed by the University of California, Davis.</div>
            <div className="repo">Repository: <a href="https://github.com/dvyno/ucdavis-grapher" className="footer-link">https://github.com/dvyno/ucdavis-grapher</a></div>
        </footer>
    );
}

export default Footer;
