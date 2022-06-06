pragma solidity >=0.4.24 <0.6.11;

contract Storage {
    address public sender;
    string public uri;
    string public hash_sha256;

    function Storage(string memory URI, string memory Hash_SHA256) public {
        sender = msg.sender;
        uri = URI;
        hash_sha256 = Hash_SHA256;
    }

    function get() public view returns (address Sender, string URI, string Hash_SHA256) {
        return (sender, uri, hash_sha256);
    }

    function updateURI(string memory URI) public {
        if (msg.sender != sender) return;  // only allow the sender to update URI
        uri = URI;
    }
}
