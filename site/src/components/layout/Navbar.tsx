import { NavLink, Link } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import styles from './Navbar.module.css';

const LINKS = [
  { to: '/',                label: 'Accueil' },
  { to: '/catalogue',       label: 'Catalogue' },
  { to: '/entreprise',      label: 'Entreprise' },
  { to: '/qui-sommes-nous', label: 'Qui sommes-nous' },
];

export function Navbar() {
  const { totalItems, open } = useCart();
  return (
    <header className={styles.header}>
      <div className={`container ${styles.inner}`}>
        <Link to="/" className={styles.logo}>Fiestalo'<span>K</span></Link>
        <nav className={styles.nav} aria-label="Navigation principale">
          {LINKS.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.to === '/'}
              className={({ isActive }) => `${styles.link} ${isActive ? styles.active : ''}`}
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
        <button className={styles.cart} onClick={open} aria-label={`Panier, ${totalItems} articles`}>
          🛒 Panier {totalItems > 0 && <span className={styles.badge}>{totalItems}</span>}
        </button>
      </div>
    </header>
  );
}
