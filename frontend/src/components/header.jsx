import './header.scss';

function Header() {

  // UTILIZAR ESTE COMOPONENTE PARA ALMACENAR LOS DATOS, DE ESTA MANERA SE PASARAN COMO PROPS
  // Y ESTARÁN DISPONIBLES EN TODOS LOS COMPONENTES

  return (
    <header className='header'>
      <nav className='header-nav'>
        <ul className='header-ul'>
        </ul>
      </nav>
    </header>
  );
}

export default Header;