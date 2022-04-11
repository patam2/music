import { Modal } from "react-bootstrap"
import React from "react";


export default class ShowModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            show: true,
        };
        this.disable = this.disable.bind(this)
    }

    disable () {
        this.props.closeFunc(false);
        this.setState({
            show: false
        });
    }

    render() { return (
        <>
        <Modal show={this.state.show}>
            <Modal.Header>
            <Modal.Title>Playlist created</Modal.Title>
            </Modal.Header>
            <Modal.Body>Hooray, your playlist has been created! Our giga-brain AI is adding songs to it, <i>right now.</i></Modal.Body>
            <Modal.Footer>
                <button onClick={this.disable} className='btn btn-primary'><a className="link-light" href={this.props.url}>Take me to it!</a></button>
                <button className='btn btn-secondary' onClick={this.disable}>IDGAF</button>
            </Modal.Footer>
        </Modal>
        </>
    )}
}