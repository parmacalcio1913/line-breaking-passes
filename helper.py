def intersects(connections_1, connections_2):
    """Detects whether or not each connection of the set of connections connections_1 intersects with
    the matching connection in the set of connections connections_2.

    Args:
        connections_1 (torch.Tensor): Tensor of shape (nb_frames, 2) containing the coordinates of a set of connections.
        connections_2 (torch.Tensor): Tensor of shape (nb_frames, 2) containing the coordinates of a set of connections.

    Returns:
        torch.Tensor: Mask containing True for all the connections in connnections_1 that intersect with the matching connection in connections_2.
    """
    dx0 = connections_1[:, 1, 0] - connections_1[:, 0, 0]
    dx1 = connections_2[1, 0] - connections_2[0, 0]
    dy0 = connections_1[:, 1, 1] - connections_1[:, 0, 1]
    dy1 = connections_2[1, 1] - connections_2[0, 1]
    p0 = dy1 * (connections_2[1, 0] - connections_1[:, 0, 0]) - dx1 * (
        connections_2[1, 1] - connections_1[:, 0, 1]
    )
    p1 = dy1 * (connections_2[1, 0] - connections_1[:, 1, 0]) - dx1 * (
        connections_2[1, 1] - connections_1[:, 1, 1]
    )
    p2 = dy0 * (connections_1[:, 1, 0] - connections_2[0, 0]) - dx0 * (
        connections_1[:, 1, 1] - connections_2[0, 1]
    )
    p3 = dy0 * (connections_1[:, 1, 0] - connections_2[1, 0]) - dx0 * (
        connections_1[:, 1, 1] - connections_2[1, 1]
    )
    return (p0 * p1 <= 0) & (p2 * p3 <= 0)