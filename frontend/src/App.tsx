import { createBrowserRouter, RouterProvider, Link, useOutlet } from 'react-router-dom'
// import LoadingView from './routes/loading/View'
import Tree from './routes/tree/View';
import PaneView from './components/PaneView';
import Pane from './components/Pane';
import List from './components/List';
import ListItem from './components/ListItem';
import About from './routes/about/View';

import './components/styles/0_colors.scss'
import './components/styles/1_base.scss'
import './components/styles/Panes.scss'
import './components/styles/Pane.scss'
import './components/styles/SideMenu.scss'
import './components/styles/Button.scss'
import "./components/styles/Dropdown.scss"

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <MainView />,
      loader: (_: any) => {
        return {
          "data":
          [
            {
              "id": 3,
              "word": "*ain",
              "language": "Proto-West-Germanic",
              "parent": 2
            },
            {
              "id": 9,
              "word": "einn",
              "language": "Old Norse",
              "parent": 2
            },
            {
              "id": 2,
              "word": "*ainaz",
              "language": "Proto-Germanic",
              "parent": "",
            },
            {
              "id": 4,
              "word": "\xc4\x81n",
              "language": "Old English",
              "parent": 3
            },
          ]
        }
      },
      children: [
        {
          path: "/about",
          element: <About />,
        },
      ]
    }
  ]);

  return (
    <>
      <RouterProvider router={router} />
    </>
  )
}

function MainView() {
  const outlet = useOutlet();

  return <PaneView>
    <Pane className={ ("side-menu " + (outlet ? " hidden" : "")) }>
      <List>
        <ListItem><Link to='/'>Forside</Link></ListItem>
        <ListItem><Link to='/about'>Om sida</Link></ListItem>
        <ListItem><Link to='/counter'>Teljar</Link></ListItem>
      </List>
      <List>
        <ListItem>Innstillingar</ListItem>
        <ListItem>Logg ut</ListItem>
      </List>
    </Pane>
    {outlet ? outlet : <Tree />}
  </PaneView>
}

export default App
